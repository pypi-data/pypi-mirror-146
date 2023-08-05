def format_histograms(df, texts = {}, fontsize = 20):
    '''
    A function used to format a pandas generic histograms
    
    Parameters
    ----------
    df : Pandas DataFrame
        Dataframe with n features to map.
    texts : dictionary
        A dictionary with labels for each histogram. Should
        consist of xaxes, titles, and yaxes.
    fontsize : int
        fontsize of the histograms
    
    Raises
    ------
    ValueError:
        if the texts parameter is empty.
    '''
    if not texts: raise ValueError("Parameter 'texts' is empty")
    histograms = df.hist(bins=25, figsize=(30, 25))
    histograms = histograms.flatten()
    for i, hist in enumerate(histograms): 
        if (i == len(histograms) - 1): break
        if ('xaxes' in texts): hist.set_xlabel(texts['xaxes'][i])
        if ('titles' in texts): hist.set_title(texts['titles'][i])
        if ('yaxes' in texts): hist.set_ylabel(texts['yaxes'][i])
        else: hist.set_ylabel('Frequency')
        for item in ([hist.title, hist.xaxis.label, hist.yaxis.label] +
             hist.get_xticklabels() + hist.get_yticklabels()):
            item.set_fontsize(fontsize)
    return histograms