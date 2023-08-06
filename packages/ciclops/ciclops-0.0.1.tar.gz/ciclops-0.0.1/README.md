# Ciclops

Cross-platform training In CLinical Outcome PredictionS (ciclops) is the winning algorithm in [2019 Malaria DREAM Challenge SubChallenge 2](https://www.synapse.org/#!Synapse:syn16924919/wiki/583955).

Ciclops performs transfer learning from one transcriptomic platform's samples to another.

## Installation

Install this package via pip:

```
pip install ciclops
```

or clone this program to your local directory:

```
https://github.com/GuanLab/Predict-Malaria-ART-Resistance.git
```

## Usage

```
python ciclops [-h] [--train_path TRAIN_PATH] [--valid_path VALID_PATH]
               [-m MODEL_TYPE] [--no_quantile] [--shap] [-n TOP_GENES]

Pipeline for building clinical outcome prediction models on training dataset and transfer learning on validation datasets.

optional arguments:
 -h, --help            show this help message and exit
 --train_path TRAIN_PATH
                       Path to your training data, in .csv format; includes sample names as first column and labels as last column
 --valid_path VALID_PATH
                       Path to your transfer validation data, in .csv format; includes sample names as first column and labels as last column
 -m MODEL_TYPE, --model_type MODEL_TYPE
                       Machine learning models to use:
                                   lgb: LightGBM;
                                   xgb: XGBoost;
                                   rf: Random Forest;
                                   gpr: Gaussian Process Regression;
                                   lr: Linear Regression;
                                   default: lgb
 --no_quantile         If specified, do not use quantile normalization.
 --shap                Conduct SHAP analysis on the training and validation set.
 -n TOP_GENES, --top_genes TOP_GENES
                       If --shap is specified, indicate number of top genes from both training and validation sets that will be compared in post-SHAP analysis.
                       Default is 20.
```

It will generate the following folders:

`./training/`: preprocessed training datasets for model training and 10-fold cross validation

`./validation/`: validation dataset for transferring test

`./params/`: trained machine learning model parameters

`./performance/`: model performance in 10-fold cross validation and transferring test

`./SHAP/`: SHAP analysis results

## References
* For the original paper, please refer to the Guan Lab's 2022 iScience paper: [Machine learning for artemisinin resistance in malaria treatment across in vivo-in vitro platforms](https://doi.org/10.1016/j.isci.2022.103910).
* STAR Protocol (TBD)
