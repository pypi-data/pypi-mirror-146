import pandas as pd
import numpy as np
import argparse

import matplotlib.pyplot as plt

import seaborn as sns


import sklearn

from sklearn.metrics import (confusion_matrix, ConfusionMatrixDisplay)


    
def plot_hist_overlay(df0, df1, columns, labels, fig_no="1",alpha=0.7, bins=5, **kwargs):
    """
    A function that plot multiple histogram for a target
    classification label against each numerical features.
    The resulting histograms will be a grid layout contained in
    one single Figure object
    PARAMETERS:
    -------
    df0:
        A pandas DataFrame that is corresponded to the label 0
    df1:
        A pandas DataFrame that is corresponded to the label 1
    columns:
        A list of column name
    labels: 
        A list of label for each of the histograms for each label
    fig_no: optional, default="1"
        A string denoting the figure number, in the case of multiple figures
    alpha: optional, default=0.7
        A float denotes the alpha value for the matplotlib hist function
    bin: optional, default=5
        An int denotes the number of bins for the matplotlib hist function
    **kwargs:
        Other parameters for the plotting function
    REQUISITES: 
    target label are binary i.e 0 or 1, negative or positive
    -------
    RETURNS:
    -------
    A matplotlib.figure.Figure object
    Examples:
    -------
    benign_cases = train_df[train_df["class"] == 0]   # df0             
    malignant_cases = train_df[train_df["class"] == 1] # df1
    plot_hist_overlay(benign_cases, malignant_cases,["unif_size"], labels=["0 - benign", "1 - malignant"]
    
    """
    # These are legacy codes are comment out in case we need to reuse in the future
    # column_name = column.title().replace("_", " ")
    # fig, ax = plt.subplots()
    # ax.hist(df0[column], alpha=alpha, bins=bins, label=labels[0], **kwargs, figure=fig)
    # ax.hist(df1[column], alpha=alpha, bins=bins, label=labels[1], **kwargs, figure=fig)
    # ax.legend(loc="upper right")
    # ax.set_xlabel(column_name)
    # ax.set_ylabel("Count")
    # ax.set_title(f"Figure {fig_no}: Histogram of {column_name} for each target class label")
    # return ax

    if not isinstance(df0, (pd.core.series.Series,
                                pd.core.frame.DataFrame, np.ndarray)):
        raise TypeError("'df0' should be of type numpy.array or pandas.Dataframe")
    if not isinstance(df1, (pd.core.series.Series,
                                pd.core.frame.DataFrame, np.ndarray)):
        raise TypeError("'df1' should be of type numpy.array or pandas.Dataframe")
    if not isinstance(columns, list):
        raise TypeError("'columns' should be of type list")
    if not isinstance(labels, list):
        raise TypeError("'labels' should be of type list")
    if not isinstance(fig_no, str):
        raise TypeError("'fig_no' should be of 'str'")

    ## other parameters are supplied into the matplotlib functions

    # To automatically calculating the size of dimension of the figures (Square shape)
    size = len(columns)
    dim = np.ceil(np.sqrt([size])).astype(int)[0]
    fig = plt.figure(1, figsize=(22,22))

    for idx, x in enumerate(columns):
        subplot=plt.subplot(dim, dim, idx+1)
        col_name = x.title().replace("_", " ")
        subplot.hist(df0[x], alpha=alpha, bins=bins, label=labels[0], **kwargs)
        subplot.hist(df1[x], alpha=alpha, bins=bins, label=labels[1], **kwargs)
        subplot.legend(loc="upper right")
        subplot.set_xlabel(col_name, fontsize=14)
        subplot.set_ylabel("Count", fontsize=14)
        subplot.set_title(f"Figure {fig_no}.{idx+1}: Histogram of {col_name} for each target class label", 
                          fontsize=14)

    return (fig, subplot)



def boxplot_plotting (num_rows,num_columns,width,height,variables,datafr,number):
    """
    A function which returns a given number of boxplots for different target  against each numerical feature. The returning objects are seaborn.boxplot types. 
    
    -------------------
    PARAMETERS:
    A dataframe containing the variables and their correspondent labels
    Variables: A list of each variable's name
    num_rows and num_columns: An integer and positive number for both num_rows and num_columns for the
    boxplot fig "canvas" object where our boxplots will go,
    width: A positive width measure 
    length: A positive length measure 
    A binary class label 
    A column array for managing variable names
    A training dataframe object
    Integer positive number for correct ordering  of graphs 
    -------------------
    REQUISITES:
    The target labels ("class label") must be within the data frame 
    The multiplication between num_rows and num_columns must return be equal to num_variables.
    It is possible for num_rows & num_columns to be values that when multiplied don't equal the "variables" numeric value,
    but that will create more boxplots which will be empty. 
    

    --------------------
    RETURNS:
    It returns a fixed number "num_variables" of boxplot objects. Each Boxplot represents both Target Class
    Labels according to a given Variable

    --------------------
    Examples

    datafr=train_df
    --------
    boxplot_plotting (3,3,20,25,numeric_column,datafr,number)
    """
    fig,ax= plt.subplots(num_rows,num_columns,figsize=(width,height))
    for idx, (var,subplot) in enumerate(zip(variables,ax.flatten())):
        a = sns.boxplot(x='class',y=var,data=datafr,ax=subplot).set_title(f"Figure {number}.{idx}: Boxplot of {var} for each target class label")
    return fig



def tuned_para_table(search, X_train, y_train):
    """
    A function which returns a panda dataframe of tuned hyperparameters
    and its best score given GridSearchCV object fitted X_train and y_train
    -------------------
    PARAMETERS:
    search: A sklearn.model_selection._search.GridSearchCV that has been
    specified estimator, param_grid, **kwargs
    X_train : numpy array or pandas DataFrame/Series
        X in the training data
    y_train : numpy array or pandas DataFrame/Series
        y in the training data
    --------------------
    REQUISITES:
    X_train, y_train must at least n_splits (specified in cv in search)
    observations for each target class.
    search must be GridSearchCV object that is clearly specified with
    estimator, param_grid, cv, and so on.
    --------------------
    RETURNS:
    Returns a pandas.core.frame.DataFrame object that specifies
    the tuned hyperaparameters and the best score produced by GridSearchCV
    --------------------
    Examples

    search = GridSearchCV(KNeighborsClassifier(),
                      param_grid={'kneighborsclassifier__n_neighbors':
                      range(1, 10)},
                      cv=10, 
                      n_jobs=-1,  
                      scoring="recall", 
                      return_train_score=True)
    --------
    tuned_para_table(search, X_train, y_train)
    """
    if not isinstance(search, sklearn.model_selection._search.GridSearchCV):
        raise TypeError("'search' should be of type GridSearchCV")
    if not isinstance(X_train, (pd.core.series.Series,
                                pd.core.frame.DataFrame, np.ndarray)):
        raise TypeError("'X_train' should be of type np.array or pd.Dataframe")
    if not isinstance(y_train, (pd.core.series.Series,
                                pd.core.frame.DataFrame, np.ndarray)):
        raise TypeError("'y_train' should be of type np.array or pd.Dataframe")
    search.fit(X_train, y_train)
    best_score = search.best_score_.astype(type('float', (float,), {}))
    tuned_para = pd.DataFrame.from_dict(search.best_params_, orient='index')
    tuned_para = tuned_para.rename(columns = {0 : "Value"})
    tuned_para = tuned_para.T
    tuned_para['best_score'] = best_score
    return tuned_para




def plot_cm(model, X_train, y_train, X_test, y_test, title):
    """
    Returns confusion matrix on predictions of y_test with given title 
    of given model fitted X_train and y_train 
    -----------
    PARAMETERS:
    model :
        scikit-learn model or sklearn.pipeline.Pipeline
    X_train : numpy array or pandas DataFrame/Series
        X in the training data
    y_train : numpy array or pandas DataFrame/Series
        y in the training data
    X_test : numpy array or pandas DataFrame/Series
        X in the testing data
    y_test : numpy array or pandas DataFrame/Series
        y in the testing data
    -----------
    REQUISITES:
    X_train, y_train, X_test, y_test cannot be empty.
    -----------
    RETURNS:
    A sklearn.metrics._plot.confusion_matrix.ConfusionMatrixDisplay object 
    -----------
    Examples
    plot_cm(DecisionTreeClassifier(), X_train, y_train, X_test, y_test, "Fig")
    """
    if not isinstance(X_train, (pd.core.series.Series,
                                pd.core.frame.DataFrame, np.ndarray)):
        raise TypeError("'X_train' should be of type numpy.array or pandas.Dataframe")
    if not isinstance(y_train, (pd.core.series.Series,
                                pd.core.frame.DataFrame, np.ndarray)):
        raise TypeError("'y_train' should be of type numpy.array or pandas.Dataframe")
    if not isinstance(X_test, (pd.core.series.Series,
                               pd.core.frame.DataFrame, np.ndarray)):
        raise TypeError("'X_test' should be of type numpy.array or pandas.Dataframe")
    if not isinstance(y_test, (pd.core.series.Series,
                               pd.core.frame.DataFrame, np.ndarray)):
        raise TypeError("'y_test' should be of type numpy.array or pandas.Dataframe")
    if not isinstance(title, str):
        raise TypeError("'title' should be of 'str'")
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    cm = confusion_matrix(y_test, predictions, labels=model.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                  display_labels=model.classes_)
    disp.plot()
    plt.title(title)
    return disp
