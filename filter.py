import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask
import numpy as np
from sklearn.feature_selection import mutual_info_regression
from sklearn.feature_selection import mutual_info_classif
import os

def read(path):
    df=pd.read_csv(path)
    return df

def preparation(dataframe):
    X = dataframe.copy()
    y = X.pop(list(X.columns)[-1])

    # Label encoding for categoricals
    for colname in X.select_dtypes("object"):
        X[colname], _ = X[colname].factorize()

    # All discrete features should now have integer dtypes (double-check this before using MI!)
    discrete_features = X.dtypes == int
    return (X,y,discrete_features)

def problem_type(target):
    if target[0] not in [0,1] and target.dtypes!=object:
        return 1 # we have a regression problem
    else:
        return 0 # we have a classification problem

def mi_scores_for_regression(X, y, discrete_features):
    mi_scores = mutual_info_regression(X, y, discrete_features=discrete_features)
    mi_scores = pd.Series(mi_scores, name="MI Scores", index=X.columns)
    mi_scores = mi_scores.sort_values(ascending=False)
    return mi_scores

def mi_scores_for_classification(X, y, discrete_features):
    mi_scores = mutual_info_classif(X, y, discrete_features=discrete_features)
    mi_scores = pd.Series(mi_scores, name="MI Scores", index=X.columns)
    mi_scores = mi_scores.sort_values(ascending=False)
    return mi_scores

def plot_mi_scores(scores,path):
    scores = scores.sort_values(ascending=True)
    width = np.arange(len(scores))
    ticks = list(scores.index)
    plt.barh(width, scores)
    plt.yticks(width, ticks)
    plt.title("Mutual Information Scores")
    if os.path.exists(path):
        return 0
    plt.savefig(path)

def filter_features(scores):
    final_scores={}
    for i in range(0,len(scores)):
        if (scores[i]>0.0001):
            final_scores[scores.index[i]]=scores[i]
    return final_scores

