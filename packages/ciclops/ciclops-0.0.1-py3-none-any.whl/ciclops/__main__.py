import numpy as np
import pandas as pd
import sys, os, pickle
import argparse, textwrap
from .preprocess import data_preparation
from .common import  build_training_model, transfer_test
from .SHAP_importance import lauch_SHAP, sum_SHAP_values_of_genes, intersect_of_top_genes

def main():
    parser = argparse.ArgumentParser(description = 'Pipeline for building clinical outcome prediction models on training dataset and transfer learning on validation datasets.',
            usage = 'use "%(prog)s --help" for more information',
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--train_path', type = str,
            help = "Path to your training data, in .csv format; includes sample names as first column and labels as last column")
    parser.add_argument('--valid_path', type = str,
            help = "Path to your transfer validation data, in .csv format; includes sample names as first column and labels as last column")
    parser.add_argument('-m','--model_type', type = str,
            help = '''Machine learning models to use:
            lgb: LightGBM;
            xgb: XGBoost;
            rf: Random Forest;
            gpr: Gaussian Process Regression;
            lr: Linear Regression;
            default: lgb''',
            default = 'lgb')
    parser.add_argument('--no_quantile',
            action = "store_true",
            help = "If specified, do not use quantile normalization.")
    parser.add_argument('--shap',
            action = 'store_true',
            help = "Conduct SHAP analysis on the validation set.")
    parser.add_argument('-n', '--top_genes', type = int,
            help = '''
            If --shap is specified, indicate number of top genes from both training and validation sets that will be compared in post-SHAP analysis.
            Default is 20.
            ''',
            default = 20)


    args = parser.parse_args()

    if args.no_quantile:
        print("Do not use normalization ...")

    if args.shap:
        print('Perform SHAP analysis after model training.')
        assert args.top_genes != None, "Must specify -n for post-SHAP analysis!"

    opts = vars(parser.parse_args())

    run(**opts)


def run(train_path, valid_path, model_type, no_quantile, shap, top_genes):

    # load training dataset
    df_train = pd.read_csv(train_path) # training dataset for building the model
    # load transfer validation dataset
    df_val = pd.read_csv(valid_path) # validation dataset for transfer testing

    # preprocess both training and validation dataset
    df_training, df_validation = data_preparation(df_train, df_val, no_quantile)
    generate_results(df_training, df_validation, model_type, '')

    if shap:
        print("Launching SHAP analysis ...")
        lauch_SHAP()
        sum_SHAP_values_of_genes()
        intersect_of_top_genes(top_genes)

def generate_results(df_training, df_validation, model_type, path_affix):
    """
    Params
    ------
    df_training: a Pandas DataFrame
    df_validation: a Pandas DataFrame
    model_type: str
    path_affix: str
    """
    #Part 1: 10-fold cross validation on training data
    eva_cv, eva_cv_conf = build_training_model(df_training, model_type)
    # Part 2: transfer testing on validation data
    eva_tv, eva_tv_conf = transfer_test(df_validation)

    # save evaluation results
    path = './'+path_affix+'performance'
    os.makedirs(path, exist_ok = True)
    eva_cv.to_csv(path+'/training_cv_results.csv', index = False)
    eva_cv_conf.to_csv(path+'/training_cv_confidence.csv', index = False)
    eva_tv.to_csv(path+'/validation_tv_results.csv', index = False)
    eva_tv_conf.to_csv(path+'/validation_tv_confidence.csv', index = False)

if __name__ == "__main__":
    main()
