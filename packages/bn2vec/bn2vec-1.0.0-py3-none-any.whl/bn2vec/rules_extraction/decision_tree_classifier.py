import os
import pathlib
import pickle

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier

from bn2vec import np, pd
from ..utils import Log
from .model_evaluation import *
from .rules_extractor import RulesExtractor


class DTC:

    def __init__(self, dataset, save_dir="../results/trees", ensemble = 'ens1', embedding = "lsf"):
        pathlib.Path(os.path.join(save_dir, "metrics")).mkdir(parents=True, exist_ok=True) 
        self.ensemble = ensemble
        self.embedding = embedding
        self.random_state = 42
        self.save_dir = save_dir
        self.dataset = dataset

    def score_thresholding(self, score_threshold):
        self.dataset.score_threshold = score_threshold
        self.dataset.y = self.dataset.y.assign(score = self.dataset.y['strict_score'].apply(lambda x: 1 if x >= self.dataset.score_threshold else 0))

    def train_singleton_dtcs(self, test_size = 0.3, balanced=True, thresh = 1, tpr_weight = 1, tnr_weight = 0):
        rules = None
        for fi in range(self.dataset.X.columns.shape[0]):
            X_train, X_test, y_train, y_test = train_test_split(
                self.dataset.X.iloc[:,[fi]],
                self.dataset.y['score'], 
                test_size=test_size, 
                random_state=self.random_state, 
                stratify=self.dataset.y['strict_score']
            )
            dtc = DecisionTreeClassifier(criterion='entropy', random_state=42, max_depth = 1, class_weight = 'balanced' if balanced else None)
            # validation = cross_val_score(dtc, X_train, y_train, cv=10, scoring= unbalance_immune_score_head)
            dtc.fit(X_train, y_train)
            extractor = RulesExtractor(dataset = self.dataset, dtc = dtc, features_names=[self.dataset.X.columns[fi]])
            new_rules = extractor.extract_rules(
                thresh = thresh,
                tpr_weight = tpr_weight,
                tnr_weight = tnr_weight
            )

            if type(new_rules) == pd.DataFrame:
                if type(rules) == pd.DataFrame:
                    rules = pd.concat([rules, new_rules], ignore_index=True)
                else:
                    rules = new_rules
            
            # y_train_pred = dtc.predict(X_train)
            # y_test_pred = dtc.predict(X_test)
            # metrics = summarize(y_train, y_test, y_train_pred, y_test_pred, validation, print_cm=False)
            # metrics.update({
            #     'feature': self.dataset.X.columns[fi]
            #     # 'rule':,
            #     # 'samples':
            # })
            
            # rules.append(list(metrics.values()))

        # if rules != []:
        #     rules = pd.DataFrame(rules, columns = list(metrics.keys())).sort_values(by = 'train-avg-recall', ascending = False)

        # rules = rules[rules['train-TPR'] == 1].sort_values(by = 'train-avg-precision', ascending = False)
        return rules.sort_values(by = 'train-avg-recall', ascending = False) if type(rules) != type(None) else None

    def __duplicate_singleton_class(self):
        y = self.dataset.y['strict_score'].unique()
        for yi in y:
            mask = self.dataset.y['strict_score'] == yi
            if self.dataset.y[mask]['strict_score'].count() == 1:
                # self.dataset.y = self.dataset.y.append([self.dataset.y[mask]], ignore_index = True)
                # self.dataset.X = self.dataset.X.append([self.dataset.X[mask]], ignore_index = True)
                self.dataset.y = pd.concat([self.dataset.y, self.dataset.y[mask]])
                self.dataset.X = pd.concat([self.dataset.X, self.dataset.X[mask]])

    def train_deep_dtcs(self, test_size = 0.3):
        self.__duplicate_singleton_class()
        X_train, X_test, y_train, y_test = train_test_split(
            self.dataset.X,
            self.dataset.y['score'],
            test_size=test_size,
            random_state=self.random_state,
            stratify=self.dataset.y['strict_score']
        )

        Log.info("Training unbalanced DTC: ")
        tree1 = DecisionTreeClassifier( criterion='entropy', random_state=self.random_state)
        tree1.fit(X_train, y_train)

        self.get_dtc_metrics(
            f"tumour.{self.ensemble}.{self.embedding}.tree1",
            tree1, 
            X_train, X_test, y_train, y_test, 
            class_names = ['bad', 'good']
        )

        Log.info("Training class-weighted DTC: ")
        tree2 = DecisionTreeClassifier( criterion='entropy', random_state=self.random_state, class_weight='balanced')
        tree2.fit(X_train, y_train)

        self.get_dtc_metrics(
            f"tumour.{self.ensemble}.{self.embedding}.tree2",
            tree2, 
            X_train, X_test, y_train, y_test, 
            class_names = ['bad', 'good']
        )

    def save_tree(self, dt, fname, feature_names, class_names = None):
        file = os.path.join(self.save_dir, f"{fname}.dot")
        dot_data = tree.export_graphviz(dt, out_file=file, feature_names= feature_names,  
                                        class_names = class_names,
                                    filled=True, rounded=True,  
                                    special_characters=True)
        png = os.path.join(self.save_dir, f"{fname}.png")
        os.system(f"dot -Tpng {file} -o {png}") 


    def get_dtc_metrics(self, tree_name, est, X_train, X_test, y_train, y_test, class_names = None):
        y_train_pred = est.predict(X_train)
        y_test_pred = est.predict(X_test)
        validation = cross_val_score(est, X_train, y_train, cv=10, scoring=unbalance_immune_score_head)
        metrics = summarize(y_train, y_test, y_train_pred, y_test_pred, validation)

        metrics.update({
            "depth": est.get_depth(),
            "#-leaves": est.get_n_leaves(),
            "#-nodes": est.tree_.node_count,
            "n-features": np.unique(est.tree_.feature).shape[0],
            "estimator": est,
            "features": self.dataset.X.columns
        })
        
        Log.info("Pickling metrics...")
        with open(os.path.join(self.save_dir, "metrics", tree_name), 'wb') as f:
            pickle.dump(metrics, f)
        Log.info("Saving the tree...")
        self.save_tree(est, tree_name, feature_names = self.dataset.X.columns, class_names = class_names)
        Log.info("Done")
        
        metrics_copy = metrics.copy()
        del metrics_copy['features']
        Log.info(pd.Series(metrics_copy))

        return metrics

