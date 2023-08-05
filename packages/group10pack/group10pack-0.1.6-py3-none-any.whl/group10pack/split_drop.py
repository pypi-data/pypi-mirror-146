import pandas as pd
from sklearn.model_selection import train_test_split

def split_drop(data, test_size, rn, col):
    
    """
    Splits the given dataset into a training set and a testing set, 
    further splitting each set into one without a specified column,
    and one with only said specified column.
    
    Parameters
    ----------
    data : Pandas DataFrame
        Dataframe to split into training and testing
    test_size : Double, value between 0 and 1
        The percentage of the input dataframe that will be used to make the testing set 
    rn : int
       A random number to make the split reprodicable
    col : String
       quoted column name of column to be dropped from 2 testing datasets and 2 testing datasets
    
    Raises
    ------
    TypeError:
        if the dataframe is not of the correct type
        if the random number is not a number
        if column name is not a string
        
    ValueError:
        if the test_size is not a number between 0-1
        if specified column is not in the dataset
        if dataset has less than 10 observations
    
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("data should be a dataframe")
    if not isinstance(rn, int):
        raise TypeError("random number should be an integer")
    if not isinstance(col, str):
        raise TypeError("column name should be quoted (a string)")
    if (not isinstance(test_size, float)):
        raise TypeError("the size of the testing set should be a float")
    if not (0.0 <= test_size and test_size <= 1.0): 
        raise ValueError("the size of the testing set should be a proportion")
        
    if not col in list(data.columns):
        raise ValueError("the specified column is not in the provided dataframe")
    if len(data) < 10:
        raise ValueError("please use a dataset with at least 10 observations")
        
        
    train, test = train_test_split(data, test_size = test_size, random_state=rn)
    X_train , Y_train = train.drop(columns = col), train[col]
    X_test, Y_test = test.drop(columns = col), test[col]
    
    return X_train, Y_train, X_test, Y_test