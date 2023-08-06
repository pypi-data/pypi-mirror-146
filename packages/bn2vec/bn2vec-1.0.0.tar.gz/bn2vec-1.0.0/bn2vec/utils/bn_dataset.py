import os

from bn2vec import pd


class BnDataset:

    def __init__(
        self,
        dataset_X,
        dataset_Y,
        score_threshold=1
    ):
        self.score_threshold = score_threshold
        self.X = pd.read_csv(dataset_X)
        self.y = pd.read_csv(dataset_Y)
        self.y = self.y.assign(score = self.y['strict_score'].apply(lambda x: 1 if x >= score_threshold else 0))
