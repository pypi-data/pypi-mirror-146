#!usr/bin/env python3
#author: @rayezh
import os, pickle
import shap
from glob import glob
from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles

def SHAP_analysis(regressor, features, feature_names):
    """ Carry out SHAP analysis of trained regressor on target dataset

    Parameters:
    -----------
    regressor:
    data: Numpy array;
        size: n*m
            n: number of instances
            m: number of features
    feature_names: list of strings
        a list of all  feature names

    Yields:
    -------
    shap_df: Pandas dataframe; n row by m column
        SHAP contribution of all features on all instances
    shap_fig: matplotlib plot file
    """
    shap_values = shap.TreeExplainer(regressor).shap_values(np.array(features))
    shap_df = pd.DataFrame(np.array(shap_values), columns = feature_names)

    shap.summary_plot(shap_values, np.array(features), feature_names = feature_names, show=False)
    shap_fig = plt.gcf()
    plt.close()

    return shap_df, shap_fig

def lauch_SHAP():
    """ Lauch SHAP Analysis on both trainnig and validation datasets
    """
    all_model_path = glob('./params/*.sav')
    training_path = './training/'
    validation_path = './validation/'

    # training datasets
    os.makedirs('./training', exist_ok = True)
    os.makedirs('./SHAP/training', exist_ok = True)
    shap_all = []
    for model_path in all_model_path:
        idx = model_path.split('/')[-1].split('_')[1] # index of fold; range from 0 to 9
        regressor = pickle.load(open(model_path, 'rb'))
        fpath = training_path+'fold_'+str(idx)+'/Test.csv'
        Test = pd.read_csv(fpath)
        Test_X = Test.iloc[:, 1:-1]
        shap_df, shap_fig = SHAP_analysis(regressor, Test_X, list(Test_X.columns))
        shap_df.to_csv('./SHAP/training/SHAP_values_'+str(idx)+'_training.csv', index = False)
        shap_fig.savefig('./SHAP/training/SHAP_importance_'+str(idx)+'.pdf', format='pdf', dpi=1200, bbox_inches='tight')
        shap_all.append(shap_df)

    shap_df = pd.concat(shap_all)
    shap_df.to_csv('./SHAP/training/SHAP_values_all_training.csv', index = False)

    # validation datasets
    os.makedirs('./validation', exist_ok = True)
    os.makedirs('./SHAP/validation', exist_ok = True)
    for model_path in all_model_path:
        idx = model_path.split('/')[-1].split('_')[1] # index of fold; range from 0 to 9
        regressor = pickle.load(open(model_path, 'rb'))
        fpath = validation_path+'Test.csv'
        Test = pd.read_csv(fpath)
        Test_X = Test.iloc[:, 1:-12] # This dataframe contains the prediction labels + ensemble prediction score (+11 columns at the end)
        shap_df, shap_fig = SHAP_analysis(regressor, Test_X, list(Test_X.columns))
        shap_fig.savefig('./SHAP/validation/SHAP_importance_'+str(idx)+'.pdf', format='pdf', dpi=1200, bbox_inches='tight')
        shap_df.to_csv('./SHAP/validation/SHAP_values_'+str(idx)+'_validation.csv', index = False)

def sum_SHAP_values_of_genes():
    """ Calculate the SHAP contributions of each gene in predictions (for both training and validation datasets)
        Sort genes by SHAP values
    """

    # training set top genes
    df_training = {'gene':[], 'SHAP_val':[], 'fold':[]}
    paths = glob('./SHAP/training/SHAP_values_*_training.csv')
    for path in paths:
        data = pd.read_csv(path, header = 0)
        idx = path.split('_')[2] # index of fold; range from 0 to 9 and all
        for col in tqdm(data.columns, total = len(data.columns.to_list())):
            gene = col
            shap_val = sum([abs(i) for i in data[col]])/len(data[col])
            df_training['gene'].append(gene)
            df_training['SHAP_val'].append(shap_val)
            df_training['fold'].append(idx)
    df_training = pd.DataFrame.from_dict(df_training)
    df_training = df_training.sort_values(by = 'SHAP_val', ignore_index = True, ascending=False)
    df_training.to_csv('./SHAP/training/SHAP_training_top_genes.csv', index = False)
    df_training_mean = df_training.groupby(['gene'])[['SHAP_val']].mean().reset_index()
    df_training_mean = df_training_mean.sort_values(by = 'SHAP_val', ignore_index = True, ascending=False)
    df_training_mean.to_csv('./SHAP/training/SHAP_training_top_genes_all_fold.csv', index = False)

    # validation set top genes
    df_validation = {'gene':[], 'SHAP_val':[], 'rep':[]}
    fpaths = glob('./SHAP/validation/SHAP_values_*_validation.csv')
    for p in fpaths:
        rep = p.split('_')[2]
        print(rep)
        data = pd.read_csv(p, header = 0)
        for col in tqdm(data.columns, total = len(data.columns.to_list())):
            gene = col
            shap_val = sum([abs(i) for i in data[col]])/len(data[col])
            df_validation['gene'].append(gene)
            df_validation['SHAP_val'].append(shap_val)
            df_validation['rep'].append(rep)
    df_validation = pd.DataFrame.from_dict(df_validation)
    df_validation.to_csv('./SHAP/validation/SHAP_validation_top_genes.csv', index = False)
    df_validation_mean = df_validation.groupby(['gene'])[['SHAP_val']].mean().reset_index()
    df_validation_mean = df_validation_mean.sort_values(by = 'SHAP_val', ignore_index = True, ascending=False)
    df_validation_mean.to_csv('./SHAP/validation/SHAP_validation_top_genes_all_fold.csv', index = False)

def intersect_of_top_genes(n):
    """ Get the intersection of top genes from training and validation sets after performing SHAP analysis.

    Parameters:
    -----------
    n: int
        the top n genes from models to find the intersection of
    """
    # Using the average SHAP value of the gene across 10 models (from 10-fold cross-validation)
    df_training_mean = pd.read_csv('./SHAP/training/SHAP_training_top_genes_all_fold.csv')
    top_training = list(df_training_mean.loc[:(n-1), 'gene'])

    df_validation_mean = pd.read_csv('./SHAP/validation/SHAP_validation_top_genes_all_fold.csv')
    top_val = list(df_validation_mean.loc[:(n-1), 'gene'])

    # Find genes in common among the top n genes from each set
    common = list(set(top_training) & set(top_val))
    # Save that to a file for future reference
    with open('./SHAP/intersection_list_top_' + str(n) + '_genes.txt', 'w') as file:
        for gene in common:
            file.write("%s\n" % gene)

    # Make Venn diagram
    n_training = n - len(common)
    n_val = n - len(common)

    plt.figure(figsize=(5,4))
    v = venn2(subsets = (n_training, n_val, len(common)), set_labels = ('Training', 'Validation'), set_colors=('yellowgreen','orange'), alpha = 0.7)
    c = venn2_circles(subsets = (n_training, n_val, len(common)), linewidth=1, color='k')
    plt.title('Intersection of top %d genes from SHAP analysis\n on training and validation sets' % n)
    plt.savefig('./SHAP/intersection_venn_top_' + str(n) + '_genes.pdf', format='pdf', dpi=1200, bbox_inches='tight')
    plt.close()
