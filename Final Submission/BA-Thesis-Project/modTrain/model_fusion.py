from sklearn.metrics import accuracy_score
import numpy as np


class FusedModel:
    def __init__(self, models):
        self._models = models
    
    def predict_proba(self, X):
        res = []
        for model, weight in self._models:
            prob = model.predict_proba(X)
            res.append(np.asarray(prob) * weight)
        res = np.asarray(res)
        return np.sum(res, axis=0) / len(self._models)
    
    def predict(self, X):
        # get fused predict probability
        fused_prob = self.predict_proba(X)
        res = []
        for one_prob in fused_prob:
            if one_prob[0] > 0.5:
                res.append(1)
            else:
                res.append(0)
        return res
        
    
def model_fusion(dt, svm, lr, X, y):
    res = None
    max_accuracy = 0
    for w_dt in np.arange(0.0, 1.0, 0.05):
        for w_svm in np.arange(0.0, 1.0 - w_dt, 0.05):
            for w_lr in np.arange(0.0, 1.0 - w_dt - w_svm, 0.05):
                fused_model = FusedModel([(dt, w_dt), (svm, w_svm), (lr, w_lr)])
                y_pred = fused_model.predict(X)
                acc = accuracy_score(y, y_pred)
                if max_accuracy is None or acc > max_accuracy:
                    max_accuracy = acc
                    res = (w_dt, w_svm, w_lr)
    return res, max_accuracy
    