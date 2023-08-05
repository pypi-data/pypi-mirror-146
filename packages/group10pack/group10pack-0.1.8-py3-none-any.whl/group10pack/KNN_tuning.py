from sklearn.model_selection import cross_validate
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
import numpy as np
import pandas as pd

def KNN_tuning(processor,X_train,Y_train,param_grid):
    """
    A function used to format a pandas generic histograms

    Parameters
    ----------
    processor: chaining of sklearn estimators
                Estimators used to transform a given dataset
    trainx: pandas DataFrame
                A dataframe that contains the training set for Ridge
    trainy: pandas Series
                A Series of classifications for a given observation
    param_grid: an list
        Series of K values to allow for hyperparameter tuning
    Raises
    ------
    TypeError:
        if the trainx is not the correct type
        if the trainy is not the correct type
    """
    
    if not isinstance(X_train,pd.DataFrame):
        raise TypeError("train_x should be data frame")
    if not isinstance(Y_train, pd.Series):
        raise TypeError("train_y should be dataSeries")
    results_dict = {
        "n_neighbours": [],
        "mean_train_score": [],
        "mean_cv_score": []
    }

    for k in param_grid["n_neighbours"]:
        knn = make_pipeline(processor, KNeighborsClassifier(n_neighbors=k, n_jobs=-1))
        scores = cross_validate(knn, X_train, Y_train, return_train_score=True)
        results_dict["n_neighbours"].append(k)
        results_dict["mean_train_score"].append(np.mean(scores["train_score"]))
        results_dict["mean_cv_score"].append(np.mean(scores["test_score"]))
    return pd.DataFrame(results_dict)