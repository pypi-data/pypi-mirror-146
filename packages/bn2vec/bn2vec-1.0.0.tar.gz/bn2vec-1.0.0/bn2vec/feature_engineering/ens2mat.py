import os

from colomoto import minibn
import pickle
from tqdm import tqdm

from bn2vec import pd
from ..utils import ConfigParser, Config
from .bn2vec import Bn2Vec


  # rsf -> relaxed structural features
# ptrns -> patterns' features
class Ens2Mat:
    def __init__(
        self,
        config_path: str = None,
        master_model_src: str = None
    ):
        ConfigParser.parse(config_path)
        self.master_model_src = master_model_src

    def __vectorize_BNs(self, bn, basedir, bundle_name, X, Y, memorize_in, memorize_all):
        bn, strict_score, fair_score = bn.split(" ")
        strict_score = float(strict_score)
        fair_score = float(fair_score)
        BN = list(minibn.BooleanNetwork(os.path.join(basedir, bundle_name, bn)).items())
        bn_graphs, bn_sequences, dnfs_data, bn_features, y = self.__vectorize_bn(BN, os.path.join(bundle_name, bn), strict_score, fair_score)
        for embedding, features in bn_features.items():
            # X[embedding] = pd.concat([X[embedding], features], axis=1, ignore_index = True)
            X[embedding].loc[len(X[embedding].index), features.index]  = features.values
        Y.loc[len(Y.index), y.index] = y.values
        if memorize_in != '' and memorize_all:
            with open(os.path.join(memorize_in, bundle_name, str.join(".", [bn.split(".")[0], 'pkl'])), "wb") as outfile:
                pickle.dump({'bn_graphs':bn_graphs, 'bn_sequences': bn_sequences, 'dnfs_data': dnfs_data}, outfile)

    def vectorize_BNs(self, basedir, bundle_name, size = 'all'):
        memorize_in = Config.Memory.hard_memory_loc
        memorize_all = Config.Memory.hard_memory
        # bundles = [f for f in os.listdir(basedir) if os.path.isdir(os.path.join(basedir, f)) and not f.startswith(".")]
        ens_name = bundle_name.replace("-", ".")
        X = {'rsf': pd.DataFrame(), 'lsf':pd.DataFrame(), 'ptrns':pd.DataFrame(), 'igf':pd.DataFrame()}
        Y = pd.DataFrame()
        # bns_data = {}
        count = 0

        if memorize_in != '':
            memorize_in = os.path.join(memorize_in, ens_name)
            try:
                os.makedirs(os.path.join(memorize_in, bundle_name))
            except Exception:
                pass
        scoresfile = bundle_name + '.scores.txt'
        with open(os.path.join(basedir, scoresfile), 'r') as file:
            lines = file.readlines()[1:]
            llines = len(lines)
            for bn in tqdm(lines[:size if size != 'all' and size <= llines else llines], desc = bundle_name):
                self.__vectorize_BNs(bn, basedir, bundle_name, X, Y, memorize_in, memorize_all)
                if count == size:
                    break
                if size != 'all':
                    count+=1
        X['ptrns'].fillna(0.0, inplace=True)
        if memorize_in != '':
            for embedding, _X in X.items():
                if _X.size != 0:
                    _X.to_csv(os.path.join(memorize_in, f"{ens_name}.{embedding}.csv"), index=False)
            Y.to_csv(os.path.join(memorize_in, f"{ens_name}.Y.csv"), index=False)
        return X,Y

    def __vectorize_bn(self, BN, bn, strict_score, fair_score):
        gen = Bn2Vec(BN)
        bn_graphs, bn_sequences, dnfs_data, bn_features = gen.generate_features()
        y = pd.Series({'bn':bn, 'strict_score':strict_score, 'fair_score':fair_score})
        return bn_graphs, bn_sequences, dnfs_data, bn_features, y

    def vectorize_bn(self, src_file, strict_score = 1, fair_score = 1):
        BN = list(minibn.BooleanNetwork(src_file).items())
        return self.__vectorize_bn(BN, src_file, strict_score, fair_score)