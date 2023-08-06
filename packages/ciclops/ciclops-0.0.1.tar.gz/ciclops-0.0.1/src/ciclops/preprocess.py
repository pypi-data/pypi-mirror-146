import numpy as np
import pandas as pd
from tqdm import tqdm
import pickle

def imputation(df):
    """ Missing value imputation.

    Parameters:
    -----------
    df: Pandas dataframe

    Yields:
    -------
    df_new: Pandas dataframe
    """

    print("Start missing value imputation ...")
    genes = df.columns[1:-1]
    #ave = {g:df[g].sum()/df[g].count() for g in genes} # compute average gene's non-missing values
    # fill missing values with gene's average exp levels
    df_new = df.copy(deep = True)
    for g in genes:
        ave = df[g].mean(skipna=True)
        df_new.loc[df_new[g].isnull(), g] = ave

    return df_new

def quantile_normalization(df1, df2):
    """ Quantile normalization cross platforms
    Parameters:
    -----------
    df1: first Pandas dataframe after imputation
    df2: second Pandas dataframe after imputation
    Yields:
    -------
    df1_new: Pandas dataframe
    df2_new: Pandas dataframe
    """

    print("Start quantile normalization ...")
    genes = df1.columns[1:-1]
    df = pd.concat([df1[genes], df2[genes]])
    sorted_matrix = np.array([sorted(row[genes].tolist()) for _,row in df.iterrows()])
    quantiled_ave = {i:j for i, j in enumerate(list(np.mean(sorted_matrix,axis = 0)))} #{rank: value}
    df1_new = []
    for i,row in df1.iterrows():
        vals = list(row[genes])
        order = {}
        for j,k in enumerate(np.argsort(vals)):
            order.update({vals[k]:j})
        ranked_genes = [quantiled_ave[order[v]] for v in vals]
        df1_new.append(list(row.iloc[:1])+ranked_genes+list(row.iloc[-1:]))
    df1_new = pd.DataFrame(df1_new, columns = list(df1.columns))
    df2_new = []
    for i,row in df2.iterrows():
        vals = list(row[genes])
        order = {}
        for j,k in enumerate(np.argsort(vals)):
            order.update({vals[k]:j})
        ranked_genes = [quantiled_ave[order[v]] for v in vals]
        df2_new.append(list(row.iloc[:1])+ranked_genes+list(row.iloc[-1:]))
    df2_new = pd.DataFrame(df2_new, columns = list(df2.columns))
    return df1_new, df2_new

def preprocess_training(df):
    """ Preprocess raw training dataset
    """
    # preprocess prediction features
    df_new = imputation(df)
    return df_new

def preprocess_validation(df):
    """ Preprocess raw validation dataset
    """
    df_new = imputation(df)
    return df_new

def data_preparation(df_training, df_validation, no_quantile = False):
    """ Preprocess of training and validation datasets
    Parameters:
    -----------
    df_training: Pandas Dataframe
        training dataset of gene expression levels
        includes sample names as first column and labels as last column
    df_validation: Pandas Dataframe
        validation dataset of gene expression levels
        includes sample names as first column and labels as last column
    if_quantile: boolean
        if quantile normalization or not
    Yields:
    -------
    df_training: Pandas Dataframe
        processed training dataset
    df_validation: Pandas Dataframe
        processed validation dataset
    """
    # remove samples without labels
    # labels assumed to be the last column
    df_training = df_training.dropna(subset = [df_training.columns[-1]])
    df_validation = df_validation.dropna(subset = [df_validation.columns[-1]])

    # find common genes
    common_genes = sorted(list(set(df_training.columns[1:-1])&set(df_validation.columns[1:-1])))
    print("Shared genes between training and validation datasets: ",len(common_genes))

    # select common columns
    # keep original structure of first column being sample name,
    # last column being label
    df_training = df_training[[df_training.columns[0]]+common_genes+[df_training.columns[-1]]]
    df_validation = df_validation[[df_validation.columns[0]]+common_genes+[df_validation.columns[-1]]]

    # preprocess training and validation datasets respectively since they contain different labels
    df_training = preprocess_training(df_training)
    df_validation = preprocess_validation(df_validation)

    # quantile normalization on both datasets
    if no_quantile:
        pass
    else:
        df_training, df_validation = quantile_normalization(df_training, df_validation)

    return df_training, df_validation
