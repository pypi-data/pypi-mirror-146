import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
import os, pickle
from scipy.stats import pearsonr, spearmanr
from .models import *
from .statistics import *

def build_training_model(df_training, model_type):
    """ Build clinical outcome prediction model and 10-fold cross validation from training dataset.
    Model parameters for each fold are saved as fold_*_model.sav

    Parameters:
    -----------
    df_training: a Pandas dataframe
        the processed training dataset
    model_type: str
        type of model to train
        'lgb': Light GBM model
        'xgb': XGboost model
        'rf': Random Forest
        'lr': Linear regression
        'gpr' gaussian process regression

    Yields:
    -------
    eva_df: a Pandas dataframe
        evaluations of training models during 10-fold cross validation
    """
    os.makedirs('./training/', exist_ok = True) # where to save the processed training datasets during 10-fold cross validation
    os.makedirs('./params/', exist_ok = True) # where to save the model params
    kf = KFold(n_splits=10, shuffle = True, random_state = 0)
    eva_df = {'fold':[], 'AUROC':[], 'AUPRC':[], 'Pearsonr':[], 'Spearmanr':[]}
    eva_conf_df = {'Pearsonr mean[95CI]':[],'Spearmanr mean[95CI]':[],'AUROC mean[95CI]':[], 'AUPRC mean[95CI]':[]}

    pred_all = []
    gs_all = []

    for i, (train_idx,test_idx) in enumerate(kf.split(df_training)):
        print('Start preparing fold', i, '...')
        path = './training/fold_'+str(i)
        os.makedirs(path, exist_ok = True)
        TRAIN = df_training.iloc[train_idx]
        TEST = df_training.iloc[test_idx]
        TRAIN.to_csv(path+"/Train.csv", index = False)
        TEST.to_csv(path+"/Test.csv", index = False)
        TRAIN_data = TRAIN.iloc[:,1:] # assuming first column is the sample name/row numbers
        TEST_data = TEST.iloc[:,1:]

        # train model on training dataset
        if model_type == 'lgb':
            predictor = train_lighgbm_model(TRAIN_data)
        elif model_type == 'xgb':
            predictor = train_xgboost_model(TRAIN_data)
        elif model_type == 'rf':
            predictor = train_rf_model(TRAIN_data)
        elif model_type == 'lr':
            predictor = train_lr_model(TRAIN_data)
        elif model_type == 'gpr':
            predictor = train_gpr_model(TRAIN_data)
        else:
            print('No model type:', model_type)

        filename = './params/fold_'+str(i)+'_model.sav'
        print(f'Saving {model_type} model ...')
        pickle.dump(predictor, open(filename, 'wb'))

        #predict on test set
        est=pickle.load(open(filename, 'rb'))
        pred=est.predict(TEST_data.iloc[:,:-1])
        pred = np.array(list(pred))
        gs = np.array(list(TEST_data.iloc[:,-1]))

        pred_all.extend(list(pred))
        gs_all.extend(list(gs))

        auroc = compute_auroc(pred,gs)
        auprc = compute_auprc(pred,gs)
        spearman_cor, _ = spearmanr(pred,gs)
        pearson_cor, _ = pearsonr(pred,gs)
        print("AUROC =", auroc, "AUPRC =", auprc,"Pearson's r =",pearson_cor, "Spearman's r =", spearman_cor)
        # save evaluations
        eva_df['fold'].append(str(i))
        eva_df['AUROC'].append(auroc)
        eva_df['AUPRC'].append(auprc)
        eva_df['Pearsonr'].append(pearson_cor)
        eva_df['Spearmanr'].append(spearman_cor)

    # Overall confidence analysis from k-fold results
    ci = 0.95

    mb, lb, ub = boostrapping_confidence_interval(pred_all, gs_all, pearsonr_cor, ci)
    print("Mean[%d%sCI] Pearson's correlation is: %.4f[%.4f, %.4f]" % (int(ci*100), '%', mb, lb, ub))
    eva_conf_df['Pearsonr mean[95CI]'].append("%.4f[%.4f, %.4f]" %(mb, lb, ub))

    mb, lb, ub = boostrapping_confidence_interval(pred_all, gs_all, spearmanr_cor, ci)
    print("Mean[%d%sCI] Spearman's correlation is: %.4f[%.4f, %.4f]" % (int(ci*100), '%', mb, lb, ub))
    eva_conf_df['Spearmanr mean[95CI]'].append("%.4f[%.4f, %.4f]" %(mb, lb, ub))

    mb, lb, ub = boostrapping_confidence_interval(pred_all, gs_all, compute_auroc, ci)
    print("Mean[%d%sCI] AUROC is: %.4f[%.4f, %.4f]" % (int(ci*100), '%', mb, lb, ub))
    eva_conf_df['AUROC mean[95CI]'].append("%.4f[%.4f, %.4f]" %(mb, lb, ub))

    mb, lb, ub = boostrapping_confidence_interval(pred_all, gs_all, compute_auprc, ci)
    print("Mean[%d%sCI] AUPRC is: %.4f[%.4f, %.4f]" % (int(ci*100), '%', mb, lb, ub))
    eva_conf_df['AUPRC mean[95CI]'].append("%.4f[%.4f, %.4f]" %(mb, lb, ub))

    eva_df = pd.DataFrame.from_dict(eva_df)
    eva_conf_df = pd.DataFrame.from_dict(eva_conf_df)

    return eva_df, eva_conf_df

def transfer_test(df_val):
    """ Transfer validation on validation dataset

    Parameters:
    -----------
    df_val: a Pandas dataframe
        preprocessed validation dataset
        first column: sample
        last column: label

    Yields:
    -------
    eva_df: a Pandas dataframe
        performance of 10 training models on validation dataset
    eva_conf_df: a Pandas dataframe
        confidence evaluations of training models on validation dataset
    """
    path = './validation/'
    os.makedirs(path, exist_ok = True)
    eva_df = {'fold':[],'Pearsonr':[],'Spearmanr':[],'AUROC':[], 'AUPRC':[]}
    eva_conf_df = {'Pearsonr mean[95CI]':[],'Spearmanr mean[95CI]':[],'AUROC mean[95CI]':[], 'AUPRC mean[95CI]':[]}

    TRANSFER = df_val.copy()
    TRANSFER_data = TRANSFER.iloc[:,1:]  # first column is sample name

    for k in range(10):
        filename = './params/fold_'+str(k)+'_model.sav'
        est=pickle.load(open(filename, 'rb'))
        predictions=est.predict(TRANSFER_data.iloc[:,:-1])
        TRANSFER['pred_'+str(k)] = predictions

        pred=predictions
        gs=TRANSFER['label'].to_list()
        # evaluations of predictions
        spearman_cor, _ = spearmanr(pred,gs)
        pearson_cor, _ = pearsonr(pred,gs)
        auroc = compute_auroc(pred,gs)
        auprc = compute_auprc(pred,gs)
        print("Pearson's r",pearson_cor,"Spearman's r = ", spearman_cor, "AUROC =", auroc, "AUPRC = ", auprc)
        eva_df['fold'].append(k)
        eva_df['Pearsonr'].append(pearson_cor)
        eva_df['Spearmanr'].append(spearman_cor)
        eva_df['AUROC'].append(auroc)
        eva_df['AUPRC'].append(auprc)

    # ensemble the predictions from all 10 models
    gs_all = TRANSFER['label'].to_list()
    pred_all = TRANSFER[['pred_'+str(k) for k in range(10)]].mean(axis = 1).to_list()
    TRANSFER['pred_ensemble'] = pred_all
    TRANSFER.to_csv(path+"Test.csv", index = False)

    # save results to table
    RESULTS = TRANSFER[[TRANSFER.columns[0]]+['pred_'+str(k) for k in range(10)]+['pred_ensemble','label']]
    RESULTS.to_csv(path+"results.csv", index = False)

    # Overall confidence analysis from k-fold results
    ci = 0.95

    mb, lb, ub = boostrapping_confidence_interval(pred_all, gs_all, pearsonr_cor, ci)
    print("Mean[%d%sCI] Pearson's correlation is: %.4f[%.4f, %.4f]" % (int(ci*100), '%', mb, lb, ub))
    eva_conf_df['Pearsonr mean[95CI]'].append("%.4f[%.4f, %.4f]" %(mb, lb, ub))

    mb, lb, ub = boostrapping_confidence_interval(pred_all, gs_all, spearmanr_cor, ci)
    print("Mean[%d%sCI] Spearman's correlation is: %.4f[%.4f, %.4f]" % (int(ci*100), '%', mb, lb, ub))
    eva_conf_df['Spearmanr mean[95CI]'].append("%.4f[%.4f, %.4f]" %(mb, lb, ub))

    mb, lb, ub = boostrapping_confidence_interval(pred_all, gs_all, compute_auroc, ci)
    print("Mean[%d%sCI] AUROC is: %.4f[%.4f, %.4f]" % (int(ci*100), '%', mb, lb, ub))
    eva_conf_df['AUROC mean[95CI]'].append("%.4f[%.4f, %.4f]" %(mb, lb, ub))

    mb, lb, ub = boostrapping_confidence_interval(pred_all, gs_all, compute_auprc, ci)
    print("Mean[%d%sCI] AUPRC is: %.4f[%.4f, %.4f]" % (int(ci*100), '%', mb, lb, ub))
    eva_conf_df['AUPRC mean[95CI]'].append("%.4f[%.4f, %.4f]" %(mb, lb, ub))

    eva_df = pd.DataFrame.from_dict(eva_df)
    eva_conf_df = pd.DataFrame.from_dict(eva_conf_df)
    return eva_df, eva_conf_df
