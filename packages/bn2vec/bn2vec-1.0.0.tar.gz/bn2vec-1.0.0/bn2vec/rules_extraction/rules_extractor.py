import pickle

from sklearn.model_selection import train_test_split

from .model_evaluation import *
from bn2vec import np, pd


class RulesExtractor:

    def __init__(self, dataset, dtc, features_names = None):
        if type(dtc) == str:
            with open(dtc, "rb") as pckl:
                tree_metrics = pickle.load(pckl)
                self.dtc = tree_metrics['estimator']
                self.features_names = tree_metrics['features']
        else:
            self.dtc = dtc
            self.features_names = features_names 
        self.random_state = 42
        self.dataset = dataset
        self.current_rule = None
        self.count = 0


    def is_discriminative_node(self, tree_, node_id, thresh = 0.8, tpr_weight = 0.5, tnr_weight = 0.5):
        # print(tree_.value)
        # norm1 = tree_.value[0,0,:n_classes - 1].sum()
        # norm2 = tree_.value[0,0,n_classes - 1]
        # val =  0.5*((1 - tree_.value[node_id,0,:n_classes - 1].sum()/norm1) + (tree_.value[node_id,0,n_classes - 1]/norm2))
        # return val >= thresh, tree_.value[node_id,0],val, 1 - tree_.value[node_id,0,:n_classes - 1].sum()/norm1, tree_.value[node_id,0,n_classes - 1]/norm2, tree_.value[0,0]
        norm1 = tree_.value[0,0,0]
        norm2 = tree_.value[0,0,1]
        val =  tnr_weight*(1 - tree_.value[node_id,0,0]/norm1) + tpr_weight*(tree_.value[node_id,0,1]/norm2)
        # return val >= thresh, tree_.value[node_id,0],val, 1 - tree_.value[node_id,0,0]/norm1, tree_.value[node_id,0,1]/norm2
        return val >= thresh, tree_.value[node_id,0]


    def predict(self, X):
        y_pred = np.repeat(True, X.shape[0])
        for rule in self.current_rule:
            y_pred = y_pred & (X[rule[0]] <= rule[2] if rule[1] == "<=" else X[rule[0]] >= rule[2]).values 

        # if self.count == 18:
        #     print(y_pred.sum())
        return np.where(y_pred, 1, 0)

    def get_rule_metrics(self, X_train, X_test, y_train, y_test, samples, rule):
        self.current_rule = rule
        y_train_pred = self.predict(X_train)
        y_test_pred = self.predict(X_test)
        # validation = cross_val_score(self, X_train, y_train, cv=10, scoring = unbalance_immune_score_head)
        metrics = summarize(y_train.values, y_test.values, y_train_pred, y_test_pred, np.array([np.nan]), print_cm=False)
        metrics.update({
            'rule': rule,
            'rule-length': len(rule),
            'samples': samples
        })
        return metrics

    def project_threshold(self, feature_name, direction, thresh):
        x = self.dataset.X[feature_name].values
        y = x - thresh
        # print(thresh, np.abs(x[y >= 0 if direction == 'up' else y <= 0]).min())
        # return thresh
        # return x[y >= 0 if direction == 'up' else y <= 0].min()
        return x[np.abs(np.where(y >= 0 if direction == 'up' else y <= 0, y, np.inf)).argmin()]

    def __duplicate_singleton_class(self):
        y = self.dataset.y['strict_score'].unique()
        for yi in y:
            mask = self.dataset.y['strict_score'] == yi
            if self.dataset.y[mask]['strict_score'].count() == 1:
                self.dataset.y = self.dataset.y.append([self.dataset.y[mask]], ignore_index = True)
                self.dataset.X = self.dataset.X.append([self.dataset.X[mask]], ignore_index = True)

    def extract_rules(self, thresh = 0.8, tpr_weight = 0.5, tnr_weight = 0.5, test_size = 0.3):
        self.__duplicate_singleton_class()
        X_train, X_test, y_train, y_test = train_test_split(
            self.dataset.X,
            self.dataset.y['score'],
            test_size=test_size,
            random_state=self.random_state,
            stratify=self.dataset.y['strict_score']
        )

        children_left = self.dtc.tree_.children_left
        children_right = self.dtc.tree_.children_right
        n_nodes =  self.dtc.tree_.node_count
        # feature_names = tree_metrics['features']
        features = self.dtc.tree_.feature
        threshold = self.dtc.tree_.threshold
        pretty_rules = {}
        good_rules = []
        node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
        is_leaf = np.zeros(shape=n_nodes, dtype=bool)
        stack = [(0, 0)]  

        while len(stack) > 0:
            node_id, depth = stack.pop()
            node_depth[node_id] = depth

            is_split_node = children_left[node_id] != children_right[node_id]

            if is_split_node:
                stack.append((children_left[node_id], depth + 1))
                stack.append((children_right[node_id], depth + 1))
            else:
                is_leaf[node_id] = True
                continue

    #         l_rule = f"{feature_names[features[node_id]]} <= {threshold[node_id]}"
    #         r_rule = f"{feature_names[features[node_id]]} > {threshold[node_id]}"
            
            up_thresh = self.project_threshold(self.features_names[features[node_id]], 'up', threshold[node_id])
            down_thresh = self.project_threshold(self.features_names[features[node_id]], 'down', threshold[node_id])
            # print(self.features_names[features[node_id]], threshold[node_id], down_thresh)
            l_rule = (self.features_names[features[node_id]], "<=", down_thresh)
            r_rule = (self.features_names[features[node_id]], ">=", up_thresh)

            if depth > 0:
                pretty_rules[children_left[node_id]] = pretty_rules[node_id].copy()
                pretty_rules[children_left[node_id]].append(l_rule)
                pretty_rules[children_right[node_id]] = pretty_rules[node_id].copy()
                pretty_rules[children_right[node_id]].append(r_rule)
            else:
                pretty_rules[children_left[node_id]] = [l_rule]
                pretty_rules[children_right[node_id]] = [r_rule]


            testpassed, samples = self.is_discriminative_node(self.dtc.tree_, children_left[node_id], thresh = thresh, tpr_weight=tpr_weight, tnr_weight=tnr_weight)
            if testpassed: 
                metrics = self.get_rule_metrics(X_train, X_test, y_train, y_test, samples, pretty_rules[children_left[node_id]])
                good_rules.append(list(metrics.values()))
                
            testpassed, samples = self.is_discriminative_node(self.dtc.tree_, children_right[node_id], thresh = thresh, tpr_weight=tpr_weight, tnr_weight=tnr_weight)
            if testpassed: 
                metrics = self.get_rule_metrics(X_train, X_test, y_train, y_test, samples, pretty_rules[children_right[node_id]])
                good_rules.append(list(metrics.values()))

        if good_rules != []:
            good_rules = pd.DataFrame(good_rules, columns = list(metrics.keys())).sort_values(by = 'train-avg-recall', ascending = False)
        
        return good_rules
