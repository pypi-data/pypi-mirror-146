from sklearn.metrics import confusion_matrix

from bn2vec import np
from ..utils import Log


def epsilon_score(y, y_pred, eps = 1e-3):
    return np.where(np.abs(y - y_pred) <= eps, 1, 0).sum()/y.shape[0]


def reg_score(y, y_pred):
    dist1 = 1 - y.values
    dist2 = y.values
    dist = np.hstack((dist1.reshape(-1,1), dist2.reshape(-1,1)))
    maxdist = dist.max(axis = 1)
    return (1 - np.abs(y - y_pred)/maxdist).mean()

def reg_score_head(estimator, X, y):
    y_pred = estimator.predict(X)
    return reg_score(y,y_pred)

def unbalance_immune_score(y,y_pred):
    cm = confusion_matrix(y, y_pred)
    score = {
        'precision': score_type(cm, 'precision'),
        'recall': score_type(cm, 'recall'),
    }
#     score['f2-score'] = 2*score['precision']['overall_score']*score['recall']['overall_score']/(score['precision']['overall_score'] + score['recall']['overall_score'])
    score['f2-score'] = cm[1,1]/(cm[1,1] + 0.2*cm[0,1] + 0.8*cm[1,0])
    score['avg-precision-recall'] = 0.5*(score['precision']['average'] + score['recall']['average'])
    return score

def unbalance_immune_score_head(estimator, X, y):
    y_pred = estimator.predict(X)
    return unbalance_immune_score(y, y_pred)['avg-precision-recall']

def score_type(cm, stype = 'recall'):
    if stype == 'recall': 
        scores = np.array([cm[i,i]/cm[i,:].sum() if cm[i,:].sum() > 0 else 0 for i in range(cm.shape[0])])
        # scores = np.array([cm[0,0]/cm[0,:].sum(), ])
    if stype == 'precision':   
        scores = np.array([cm[i,i]/cm[:,i].sum() if cm[:,i].sum() > 0 else 0 for i in range(cm.shape[0])])
    
    return {
        'per-class': scores,
        'average': scores.mean()
    }


def summarize(y_train, y_test, y_train_pred, y_test_pred, validation, print_cm=True):
    train_tree_metrics = unbalance_immune_score(y_train, y_train_pred)
    test_tree_metrics = unbalance_immune_score(y_test, y_test_pred)
    if print_cm:
        Log.info("Train CM : \n")
        Log.info(confusion_matrix(y_train, y_train_pred))
        Log.info("Test CM : \n")
        Log.info(confusion_matrix(y_test, y_test_pred))

    metrics =  {
        "train-avg-precision": train_tree_metrics['precision']['average'], 
        "train-avg-recall": train_tree_metrics['recall']['average'],
        "train-f2-score": train_tree_metrics['f2-score'], 
        "train-avg-precision-recall": train_tree_metrics['avg-precision-recall'], 
        "train-TNR": train_tree_metrics['recall']['per-class'][0], 
        "train-TPR": train_tree_metrics['recall']['per-class'][1], 
        "avg-cv-score": validation.mean(),
        "std-cv-score": validation.std(),
        "test-avg-precision": test_tree_metrics['precision']['average'], 
        "test-avg-recall": test_tree_metrics['recall']['average'],
        "test-f2-score": test_tree_metrics['f2-score'], 
        "test-avg-precision-recall": test_tree_metrics['avg-precision-recall'], 
        "test-TNR": test_tree_metrics['recall']['per-class'][0], 
        "test-TPR": test_tree_metrics['recall']['per-class'][1], 
    }

    return metrics