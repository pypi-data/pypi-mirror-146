import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def inv_outcome_plot(grouped_df: pd.DataFrame,
                      size_col: str,
                      bar_split_col: str,
                      val_col: str, 
                      counts_col: str,
                     major_earner: bool,
                     fig_title: str,
                     fig_ylabel: str):
    
    """
    The function inv_outcome_plot generates a normalized stacked bar charts showing proportions of 
    major earner/non major earner individuals that made money on investments 
    and proportion of individuals that lost money on investments among families 
    of different size
    
    Parameters
    ----------
    grouped_df : Pandas DataFrame
        Dataframe grouped by size.
    size_col : String
        name of column of integers corresponding to family sizes
    bar_split_col : String
        name of column of binary integers corresponding to variable stacked bar chart is split on
    val_col : String
        name of column of boolean corresponding to results of investments given in boolean
        NOTE: this can be the predicted values from model, or actual values from data
    counts_col : String
        name of column of integers corresponding to counts of each group
    major_earner : Boolean
        True indicates plots portray investment income outcome data for major income earners, 
        False indicates plots portray investment income outcome for non major income earners
    fig_title : String
        name of figure
    fig_ylabel : String
        name of y axis of stacked bar chart plot
    
    
    Raises
    ------
    TypeError:
        if grouped_df is not a DataFrame
        if size_col is not a String
        if grouped_df[size_col] is not a column of integers
        if bar_split_col is not a String
        if grouped_df[bar_split_col] is not a columns of binary integers (2 integers)
        if val_col is not a String
        if grouped_df[val_col] is not a column of boolean
        if counts_col is not a String
        if grouped_df[counts_col] is not a column of integers
        if major_earner is not a Boolean
        if fig_title is not a String
        if fig_ylabel is not a String
    """
    if not isinstance(grouped_df, pd.DataFrame):
        raise TypeError("grouped_df is not a DataFrame")
    if not isinstance(size_col, str):
        raise TypeError("size_col is not inputted as String")
    if not isinstance(bar_split_col, str):
        raise TypeError("bar_split_col is not inputted as String")
    if not isinstance(val_col, str):
        raise TypeError("val_col is not inputted as String")
    if not isinstance(counts_col, str):
        raise TypeError("counts_col is not inputted as String")
    if not isinstance(major_earner, bool):
        raise TypeError("major_earner is not inputted as Boolean")
    if not isinstance(fig_title, str):
        raise TypeError("fig_title is not inputted as String")
    if not isinstance(fig_ylabel, str):
        raise TypeError("fig_ylabel is not inputted as String")

    if grouped_df[size_col].dtypes !=  "int64":
        raise TypeError("size_col must be column of integers")
    if grouped_df[bar_split_col].dtypes !=  "int64" or grouped_df[bar_split_col].nunique() != 2:
        raise TypeError("bar_split_col must be a binary column of integers with only 2 distinct values")
    if grouped_df[val_col].dtypes !=  "bool":
        raise TypeError("val_col must be column of boolean")
    if grouped_df[counts_col].dtypes !=  "int64":
        raise TypeError("counts_col must be column of integers")
            
    family_sizes = [1, 2, 3, 4, 5, 6, 7]
    
    all_maj_earners = grouped_df[grouped_df[bar_split_col] == 1]
    all_non_earners = grouped_df[grouped_df[bar_split_col] == 2]
    
    list_of_fam_size_df = []
    made_money_pctg = []
    not_made_money_pctg = []
    
    if major_earner:
        for i in range(7):
            list_of_fam_size_df.append(all_maj_earners[all_maj_earners[size_col] == i+1])
            list_of_fam_size_df[i][counts_col] = list_of_fam_size_df[i][counts_col].div(np.sum(list_of_fam_size_df[i][counts_col]))
            made_money_pctg.append(list_of_fam_size_df[i][list_of_fam_size_df[i][val_col]==True].counts.sum())
            not_made_money_pctg.append(list_of_fam_size_df[i][list_of_fam_size_df[i][val_col]==False].counts.sum())                  
    else:
        for i in range(7):
            list_of_fam_size_df.append(all_non_earners[all_non_earners[size_col] == i+1])
            list_of_fam_size_df[i][counts_col] = list_of_fam_size_df[i][counts_col].div(np.sum(list_of_fam_size_df[i][counts_col]))
            made_money_pctg.append(list_of_fam_size_df[i][list_of_fam_size_df[i][val_col]==True].counts.sum())
            not_made_money_pctg.append(list_of_fam_size_df[i][list_of_fam_size_df[i][val_col]==False].counts.sum())   
    
    width = 0.35
    fig, ax = plt.subplots()

    ax.bar(family_sizes, made_money_pctg, width, label="Money made on investments")
    ax.bar(family_sizes, not_made_money_pctg, width, bottom=made_money_pctg,
       label="No money made on investments")
    
    ax.set_xlabel("Family Size")
    ax.set_ylabel(fig_ylabel)
    ax.set_title(fig_title)
    ax.legend()
    
    return fig
        