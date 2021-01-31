from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC


# Train model on DT estimator
def train_decision_tree_model(X_train, y_train, cv=10):
    models = []
    scores = []
    for max_depth in range(3, 15):
        decision_tree_clf = DecisionTreeClassifier(random_state=0, max_depth=max_depth)
        score = cross_val_score(decision_tree_clf, X_train, y_train, cv=cv)
        models.append(decision_tree_clf)
        scores.append(score)
    return models, scores

# Train model on SVM estimator
def train_svm_model(X_train, y_train, cv=10):
    models = []
    scores = []
    for reg_C in [1e-4, 1e-3, 1e-2, 0.1, 1, 10]:
        svm_clf = SVC(C=reg_C, kernel='rbf', gamma='auto')    
        score = cross_val_score(svm_clf, X_train, y_train, cv=cv)
        models.append(svm_clf)
        scores.append(score)
    return models, scores

# Train model on LR estimator
def train_logistic_regression_model(X_train, y_train, cv=10):
    models = []
    scores = []
    for reg_C in [1e-4, 1e-3, 1e-2, 0.1, 1, 10]:
        lr_clf = LogisticRegression(random_state=0, penalty='l2', C=reg_C).fit(X_train, y_train)  
        score = cross_val_score(lr_clf, X_train, y_train, cv=cv)
        models.append(lr_clf)
        scores.append(score)
    return models, scores
    

