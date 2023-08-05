import pandas as pd
import sklearn
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import RidgeCV

def ridge_alpha_tuning(alpha, processor, trainx, trainy, cv=10):
    """
    A function used to format a pandas generic histograms

    Parameters
    ----------
    alpha: List of integer
            A list of Hyperparameter used to tune Ridge
    processor: chaining of sklearn estimators
                Estimators used to transform a given dataset
    trainx: pandas DataFrame
                A dataframe that contains the training set for Ridge
    trainy: pandas Series
                A Series of classifications for a given observation
    cv: An integer
            Integer represent the number of cross validation
    Raises
    ------
    TypeError:
        if the alpha is not the correct type
        if the cv is not the correct type
        if the trainx is not the correct type
        if the trainy is not the correct type
    """
    if not isinstance(alpha, list):
        raise TypeError("alpha is not a list")
    if not isinstance(trainx, pd.DataFrame):
        raise TypeError("train_x should be data frame")
    if not isinstance(trainy, pd.Series):
        raise TypeError("train_y should be data frame")
    if not isinstance(cv,int):
        raise TypeError("cv should be an integer")
    ridge_cv_pipe = make_pipeline(processor, RidgeCV(alphas=alpha, cv=cv))
    ridge_cv_pipe.fit(trainx, trainy)
    best_alpha = ridge_cv_pipe.named_steps["ridgecv"].alpha_
    return best_alpha
