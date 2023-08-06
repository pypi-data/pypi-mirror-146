from igraph import Graph

from bn2vec import np, pd
from ..utils import Log
from ..bn2vec_exceptions import FeatureSelectorModeUnaccetableException


class BnFeaturesSelector:
    # features with their explainability importance :
    features = {
        'min': 1, '2nd-order-stat': 1, 'max': 1, 'range': 1,
        'entropy': 0.33, 'std': 0.66, 'mode': 0.66, '25%': 0.33,
        '50%': 0.20, '75%': 0.33, 'IQ-range': 0.33
    }
    features.update(
        {'moment2': 0, 'moment3': 0}
    )
    features['moment1'] = 1
    seqs = {
        'degrees': 0.66, 'weights': 0.66, 'cc': 0,
        'cdegrees': 0.66, 'vdegrees': 0.66, 'notseq': 1
    }
    graphs = {
        'vcp': 1, 'vcn': 1, 'vgp': 0.66, 'vgn': 0.66,
        'vgos': 0.66, 'cgp': 0.55, 'cgn': 0.55,
        'compdnfp': 1, 'compdnfn': 1, 'compgp': 0.66,
        'compgn': 0.66, 'compgos': 0.66, 'dnfgp': 0.55,
        'dnfgn': 0.55, 'dnfgos': 0.55, 'notgraph': 1
    }

    def __init__(
        self,
        X,
        mode='lossy'
    ):
        self.X = X
        self.nbr_features = len(self.X.columns)
        self.mode = mode
        self._validate()

    def _validate(self):
        if self.mode not in ['lsf', 'rsf', 'igf', None]:
            raise FeatureSelectorModeUnaccetableException(self.mode)

    def drop_zero_variance_features(
        self,
        epsilon=1e-4
    ):
        stds = self.X.std()
        novar = stds[stds <= epsilon]
        self.X = self.X[[c for c in self.X.columns if c not in novar.index]]
        self.nbr_features -= len(novar.index)
        return self.X

    # we select the features based on their explainability importance (and possibly later, their correlation)
    # Importance(f) = (0.2 * SeqImportance(f) + 0.45 * DnfStatisticImportance(f) + 0.35 * BnStatisticImportance(f))/3
    def __lossy_sf_collinear_importance(self, feature):
        f_tokens = feature.split("_")
        graph_impo = self.graphs['notgraph' if 'cv' in f_tokens[0] else f_tokens[0]]
        seq_impo = self.seqs['notseq' if 'cv' in f_tokens[0] else f_tokens[1]]
        dnf_stat_impo = self.features[f_tokens[1] if 'cv' in f_tokens[0] else f_tokens[2]]
        bn_stat_impo = self.features[f_tokens[1] if 'cv' in f_tokens[0] else f_tokens[3]]
        return 0.125*graph_impo + 0.325*seq_impo + 0.25*dnf_stat_impo + 0.25*bn_stat_impo

    def __relaxed_sf_collinear_importance(self, feature):
        f_tokens = feature.split("_")
        graph_impo = self.graphs['notgraph' if 'cv' in f_tokens[1] else f_tokens[1]]
        seq_impo = self.seqs['notseq' if 'cv' in f_tokens[1] else f_tokens[2]]
        dnf_stat_impo = 1 if 'cv' in f_tokens[1] else self.features[f_tokens[3]]
        return 0.2*graph_impo + 0.5*seq_impo + 0.3*dnf_stat_impo

    def __igf_sf_collinear_importance(self, feature):
        f_tokens = feature.split("_")
        graph_impo = self.graphs['notgraph' if 'cv' in f_tokens[0] else f_tokens[0]]
        seq_impo = self.seqs['notseq' if 'cv' in f_tokens[0] else f_tokens[1]]
        stat_impo = self.features[f_tokens[1] if 'cv' in f_tokens[0] else f_tokens[2]]
        return 0.225*graph_impo + 0.425*seq_impo + 0.3*stat_impo

    def __collinear_importance(self, feature):
        if self.mode == 'lsf':
            return self.__lossy_sf_collinear_importance(feature)
        elif self.mode == 'igf':
            return self.__igf_sf_collinear_importance(feature)
        elif self.mode == 'rsf':
            return self.__relaxed_sf_collinear_importance(feature)

    def correlated_based_clustering_cost(self, corr_thresh, labels):
        withincost = 0
        betweencost = 0
        nclusters = np.unique(labels).shape[0]
        clusters = np.unique(labels)

        for i in range(nclusters):
            left = (labels == clusters[i])
            left_sum = left.sum()
            for j in range(i + 1, nclusters):
                right = (labels == clusters[j])
                # between cost
                betweencost += corr_thresh.loc[left, right].values.sum()/(left_sum * right.sum())
            # within cost
            withincost += 1 - corr_thresh.loc[left, left].values.sum()/left_sum**2

        withincost = np.round(withincost*100/nclusters, decimals = 4)
        betweencost = np.round(betweencost*100/(nclusters*(nclusters*0.5 - 1)), decimals = 4)
        cost = np.round(0.5*betweencost + 0.5*withincost, decimals = 4)
        Log.info(f"\nWITHIN COST : {withincost}% \nBETWEEN COST : {betweencost}% \nCLUSTERING COST : {cost}% (perc of wrongdoings)")
        return withincost, betweencost, cost

    def cluster_collinear_features_leiden(
        self,
        corr=None,
        thresh=0.7,
        resolution_parameter=0.8,
        calculate_the_cost=True,
        ask_before_procceding=True
    ):
        corr_thresh = (np.abs(self.X.corr()) if corr == None else corr) >= thresh
        g = Graph()
        g.add_vertices(self.nbr_features)
        g = g.Adjacency(corr_thresh.values.tolist()).as_undirected()
        coms = g.community_leiden(resolution_parameter=resolution_parameter)
        Log.info(coms.summary())
        if calculate_the_cost:
            _, _, _ = self.correlated_based_clustering_cost(corr_thresh, np.array(coms.membership))

        if ask_before_procceding and str.upper(input("Procceed? (Y/y/N/n)")) == "N": return self.X

        clusters = np.array(coms.membership)
        return self.drop_collinear_features(corr_thresh, clusters)

    def select_based_on_explainability_importance(self, features):
        get_importance = lambda feature: self.__collinear_importance(feature)
        np_get_importance = np.vectorize(get_importance)
        best_feature = np.argmax(np_get_importance(features))
        return features[best_feature]

    def drop_collinear_features(self, corr_thresh, clusters):
        clustered_features = pd.DataFrame(self.X.columns, columns = ['feature']).assign(cluster = clusters)
        best_features = clustered_features.groupby('cluster')['feature'].apply(
            lambda features: self.select_based_on_explainability_importance(features.values)
        ).values

        self.X = self.X[best_features]
        self.nbr_features -= best_features.shape[0]

        return self.X, clusters

    def correct_collinearity(
        self,
        features,
        all_features,
        corr=None,
        thresh=0.75,
    ):
        corr = self.X.corr() if corr == None else corr
        isquart = lambda feature : ('%' in feature) or ('IQ' in feature)
        new_features = [] 
        get_importance = lambda feature: self.__collinear_importance(feature)
        np_get_importance = np.vectorize(get_importance)

        for feature in features:
            ccorr = corr.loc[[feature], all_features]
            ccorr = ccorr[np.abs(ccorr) >= thresh].dropna(axis = 1)
            if ccorr.empty:
                new_features.append(feature)
                continue
            ccorr.index = ['corr']
            ccorr.loc['imp'] = np_get_importance(ccorr.columns.values)
            cccorr = ccorr[[c for c in ccorr.columns if (c != feature) and isquart(feature) and (not isquart(c))]].T
            if cccorr.empty:
                new_features.append(feature)
                continue
            feature_total_imp = np.round(0.5*cccorr['corr'] + 0.5*cccorr['imp'], decimals = 2)
            best_features = np.round(ccorr[feature_total_imp[feature_total_imp == feature_total_imp.max()].index].T['corr'], decimals = 2)
            best_feature = best_features.index[best_features.argmax()]
            new_features.append(best_feature if ccorr.loc['imp', best_feature] > ccorr.loc['imp', feature] else feature)
        return new_features
