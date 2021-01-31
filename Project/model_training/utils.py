import itertools

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

import pickle

def load_data():
    # load data
    var1_head = ['team%d_pick%d' % (i,j) for i in range(2) for j in range(1, 6)]
    var2_head = ['team%d_ban%d' % (i,j) for i in range(2) for j in range(1, 6)]
    var_head = var1_head + var2_head
    head = var_head + ['label']
    file = 'out.csv'
    df = pd.read_csv(file, header=None, names=head, dtype='Int64')
    df.dropna(inplace=True)
    print(df.shape)
    return df

def get_metrics(model, data):
    X_test, y_test = data
    # get confusion matrix
    print(X_test.shape)
    y_pred = model.predict(X_test)
    c_mat = confusion_matrix(y_test, y_pred)
    print(c_mat)

def draw_roc_auc(model, data, model_name):
    X_test, y_test = data
    y_score = model.predict_proba(X_test)
    fpr, tpr, threshold=roc_curve(y_test, y_score[:, 1])
    
    roc_auc=auc(fpr,tpr)
    plt.figure(figsize=(10,10))
    plt.plot(fpr, tpr, color='darkorange',
    lw=2, label='ROC curve (area = %0.2f)' % roc_auc) 
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC curve of {}'.format(model_name))
    plt.legend(loc="lower right")
    plt.savefig(model_name)
    plt.show()

def get_2combine(data, suffix='_0', hash_dict=None):
    res = dict()
    for i, x in enumerate(itertools.combinations(data.to_list(), 2)):
        h_value = hash(str(x))
        if h_value not in hash_dict:
            hash_dict[h_value] = x
        res['hash_%d_%s' % (i, suffix)] = h_value
    return res


def save_as_pickle(model, model_filename='default_model.pkl'):
    with open(model_filename, 'wb') as f:
        pickle.dump(model, f)

def load_from_pickle(model, model_filename):
    try:
        with open(model_filename, 'rb') as f:
            model = pickle.load(f)
        return model
    except:
        return None