import matplotlib.pyplot as plt
import multiprocessing
import numpy as np
import pandas as pd
import seaborn as sns
import shap
import time
from azureml.core import Run
from catboost import CatBoostRegressor
from concurrent import futures 
from imblearn.over_sampling import SMOTE
from lightgbm import LGBMRegressor
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_squared_log_error, mean_absolute_percentage_error
from sklearn.model_selection import cross_val_predict
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, BaggingRegressor, StackingRegressor


class Regressor:
        
    dict_regressors = {
        "LR": LinearRegression(),
        "Lasso": Lasso(),
        "SVR_linear": SVR(kernel='linear'),
        "SVR_poly": SVR(kernel='poly'),
        "SVR_default": SVR(),
        "LGBMR": LGBMRegressor(),
        "DTR": DecisionTreeRegressor(),
        "RFR": RandomForestRegressor(),
        "Bagging": BaggingRegressor(),
        "Extra": ExtraTreesRegressor(),
        "CatBoost": CatBoostRegressor(loss_function='RMSE', silent=True)
    }

    def __init__(self, data, keep_cols, target, online=False, verbose=True):
        """ construction of Regressor class 
        """
        self.data = data
        self.target = target
        self.keep_cols = keep_cols
        if verbose:
            print("Regressor initialized")
        self.split_x_and_y(verbose)
        self.online_run = online
        if self.online_run:
            self.run = Run.get_context()

    def split_x_and_y(self, verbose=True):
        """ split target from the data 
        """
        self.features = list(set(self.data.columns.tolist()) - set(self.keep_cols) - set([self.target]))
        if verbose:
            print("Training will be done using the following features:\n", self.features)
        self.X = self.data[self.features].copy()
        self.y = self.data[self.target].copy()
        if verbose:
            print("Data is split into X and y:\n",
                "\tX:", self.X.shape, "\n",
                "\ty:", self.y.shape)

    def oversampling(self):
        """ oversampling method for imbalanced data
        """
        over = SMOTE(k_neighbors=25)
        self.X, self.y = over.fit_resample(self.X, self.y)
        print("After oversampling:\n",
              "\tX:", self.X.shape, "\n",
              "\ty:", self.y.shape, "\n")

    def experiment_models(self, cv=5, ratio_reg=False, calc_col=""):
        """ experiment the bunch of regression models for the problem
        """
        # check model performances with parallel computing
        cores = multiprocessing.cpu_count()
        workers = round(cores/2)
        df_scores = pd.DataFrame(columns = ['model', 'MAE', 'RMSE', 'R2', 'MAPE'])
        with futures.ProcessPoolExecutor(max_workers=workers) as executor:
            jobs = {}
            for model, model_instantiation in self.dict_regressors.items():
                try:
                    print(f'Model {model} is training:')
                    job = executor.submit(self.cv_score_model, model_instantiation, cv, ratio_reg, calc_col)
                except Exception as e:
                     print(model, "raises an exception while traning:", e)
                     continue
                jobs[job] = model
                time.sleep(1)  # this is just to make the output look nicer                
            for job in futures.as_completed(jobs):
                model = jobs[job]
                try:
                    scores = job.result()
                    print(f"{model} scores:")
                    [print('\t', key,':', val) for key, val in scores.items()]
                    if self.online_run:
                        [self.run.log(f"{key}:", val) for key, val in scores.items()]       
                    score_entry = {'model': model, 'MAE': scores["MAE"], 
                                   'RMSE': scores["RMSE"], 'R2': scores["R2"], 'MAPE': scores["MAPE"]}
                    df_scores = df_scores.append(score_entry, ignore_index = True)
                except Exception as e:
                     print(model, "raises an exception while scoring:", e)
                     continue
        # sort score dataframe by MAPE
        df_scores.sort_values('MAPE', ascending=True, inplace=True)
        # best models => base models for stacking
        self.base_models = [(df_scores.iloc[0].model, self.dict_regressors[df_scores.iloc[0].model]),
                            (df_scores.iloc[1].model, self.dict_regressors[df_scores.iloc[1].model]),
                            (df_scores.iloc[2].model, self.dict_regressors[df_scores.iloc[2].model])]
        # set best model
        self.best_model = self.base_models[0]

    def cv_score_model(self, model, cv=5, ratio_reg=False, calc_col=""):
        """ do a cross validation scoring with given model if no 
            model is given then a logistic regression will be tried
        """
        if model == "lr":
            model = LinearRegression()
        elif model == "best":
            model = self.best_model
        elif model == "stack":
            model = self.stacking_model()
        self.pred_test = cross_val_predict(model, self.X, self.y, cv=cv) 
        self.model = model
        y =  self.y.copy()
        pred_test = self.pred_test.copy()
        if ratio_reg:            
            pred_test = self.X[calc_col] / pred_test
            y = self.X[calc_col] / y
        scores = {}
        scores["MAE"] = round(mean_absolute_error(y, pred_test), 3)  
        scores["RMSE"] = round(mean_squared_error(y, pred_test, squared=False), 3) 
        scores["R2"] = round(r2_score(y, pred_test), 3)    
        scores["MAPE"] = round(mean_absolute_percentage_error(y, pred_test), 3) 
        return scores

    def define_base_models(self, base_list):
        """ give a list of model abbreviations to be used
            in stacking
        """
        self.base_models = []
        for name in base_list:
            self.base_models.append((name, self.dict_regressors[name]))
        print("Base models are defined!")

    def stacking_model(self):
        """ create a stacking model using best 3 base models
            that are defined after experimenting all models
        """
        if hasattr(self, 'base_models'): 
            meta_model = LinearRegression()
            final_model = StackingRegressor(estimators=self.base_models, final_estimator=meta_model, cv=5)
            return final_model
        else:
            raise AssertionError("Please first experiment models to set top 3 base models!")

    def train_model(self, model=None):
        """ train the given classification model on whole data
        """   
        if model is None:
            if hasattr(self, 'model'): 
                model = self.model
            else:
                raise AssertionError("Please pass over a model to proceed!")
        if model == "lr":
            model = LinearRegression()
        elif model == "best":
            model = self.best_model
        elif model == "stack":
            model = self.stacking_model()
        model.fit(self.X, self.y)
        print("Model is fit on whole data!")
        self.model = model

    def explain_model_with_shap(self, model=None):
        """ show SHAP values to explain the output of the regression model
        """
        if model is None:
            if hasattr(self, 'model'): 
                model = self.model
            else:
                raise AssertionError("Please pass over a model to proceed!")
        # fit the model
        self.train_model(model)
        # set important features
        importances = model.feature_importances_
        sorted_idx = importances.argsort()[(-1*self.X.shape[1]):]
        important_features = self.X.columns[sorted_idx].tolist() 
        # get shap summary plot
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(self.X)
        shap.summary_plot(shap_values, self.X, feature_names = important_features)

    def residual_difference(self, lower_threshold=0.4, higher_threshold=2.5, res=0.05, name='', ratio_reg=False, calc_col=""):
        """ show histogram distribution of the ratio between
            selected two continuous columns in the dataframe
            that wanted to be same in ideal case 
        """
        if hasattr(self, 'pred_test'): 
            df_ratio = self.data.rename(columns={self.target: "actual"})
            df_ratio["prediction"] = self.pred_test
            if ratio_reg:            
                df_ratio["prediction"] = df_ratio[calc_col] / self.pred_test
                df_ratio["actual"] = df_ratio[calc_col] / self.y
            df_ratio["error_rate"] = np.absolute(df_ratio["prediction"] - df_ratio["actual"])/df_ratio["actual"]
            # regression metrics
            metrices = apply_regression_metrics(df_ratio["actual"], df_ratio["prediction"])
            [print(key,':', val) for key, val in metrices.items()]
            if self.online_run:
                [self.run.log(f"{key}:", val) for key, val in metrices.items()]     
            # take the ratio
            df_ratio["ratio"] = df_ratio["prediction"] / df_ratio["actual"]
            df_ratio_ = df_ratio[(df_ratio["ratio"] > lower_threshold) & (df_ratio["ratio"] < higher_threshold)]
            print(f"{df_ratio_['prediction'].shape[0]} out of {len(self.pred_test)} the entries are within given ratio threshold {lower_threshold} - {higher_threshold}")
            # set ratio intervals
            df_ratio["interval"] = df_ratio["ratio"].apply(set_interval)
            print("Value counts of the ratio intervals:")
            print(df_ratio["interval"].value_counts())
            # histogram distribution
            plt.figure(figsize=(12, 9))
            sns.histplot(data=df_ratio.iloc[df_ratio_.index], x="ratio", hue="interval", binwidth=res,
                         palette={"very_high":"#205072", 
                                  "high": "#329D9C", 
                                  "medium":"#56C596",
                                  "low":"#7BE495",
                                  "very_low":"#CFF4D2"})
            plt.show()
            # regression plot of the ratio
            plt.figure(figsize=(12, 9))
            ax = sns.regplot(x=df_ratio['actual'], y=df_ratio['ratio'], order=2)
            ax.set_xlabel('target value')
            ax.set_ylabel('residual ratio')
            plt.show()            
            # plot regression plot in colors
            plt.figure(figsize=(12, 9))
            palette={"very_high":"#234c6f", 
                     "high": "#2f6694", 
                     "medium":"#5b97ca",
                     "low":"#a5c6e2",
                     "very_low":"#caddee"}
            ax = sns.regplot(x=df_ratio['prediction'], y=df_ratio['actual'], order=2)
            ax = sns.scatterplot(data=df_ratio, x="prediction", y="actual", hue="interval", palette=palette)
            ax.set_xlabel('prediction')
            ax.set_ylabel('target value')
            plt.show()
            # save figure if on cloud
            if self.online_run:
                filename=f'./outputs/{name}.png'
                plt.savefig(filename, dpi=600)
                plt.close()
            return df_ratio
        else:
            raise AssertionError("Please first have predictions to check the distribution and scoring metrics!")

    def reg_plot(self):
        """ relationship btw. predicted and actual values
        """
        plt.figure(figsize=(15, 12))
        ax = sns.regplot(x=self.pred_test, y=self.y, order=2)
        ax.set_xlabel('prediction')
        ax.set_ylabel('target value')
        plt.show()

    def quantile_regression(self, q_min = 0.05, q_max = 0.95): 
        """ quantile regression with given min/max quantiles
        """
        df = pd.DataFrame({"actual": self.y})
        for q in [q_min, 0.5, q_max]:
            scores = self.cv_score_model(LGBMRegressor(objective = 'quantile', alpha = q))
            df[f"{q}_reg"] = self.pred_test
            if q == 0.5:
                [print('\t', key,':', val) for key, val in scores.items()]
                if self.online_run:
                    [self.run.log(f"{key}:", val) for key, val in scores.items()]  
                df[f"error_rate"] = round(np.absolute(self.pred_test - self.y)/self.y, 3) 
        # evaluate result
        df["prediction"] = np.where(((df[f"{q_min}_reg"] <= df["actual"]) & (df[f"{q_max}_reg"] >= df["actual"])), True, False)
        df["range"] = df[f"{q_max}_reg"] - df[f"{q_min}_reg"]
        # plot the regression line on 0.5 quantile and predictions
        plt.figure(figsize=(12, 9))
        palette={True:"#234c6f", 
                 False:"#a5c6e2"}
        ax = sns.regplot(x=df['0.5_reg'], y=df['actual'], order=2, scatter_kws={'alpha':0.1})
        ax = sns.scatterplot(data=df, x="0.5_reg", y="actual", hue="prediction", palette=palette, alpha=0.5)
        ax.set_xlabel('0.5_reg')
        ax.set_ylabel('target value')
        plt.show()
        print("{:.1%}".format(df[df.prediction == True].shape[0] / df.shape[0]), "of the actual values are in the given range")
        print(round(df["range"].mean(), 2), "is the mean difference of the given min/max range")
        return df

    def classification_score_metrics(self):
        """ show relevant classification score metrics for the test data
        """
        if hasattr(self, 'pred_test'):  
            metrices = apply_classification_metrics(self.y, self.pred_test)
            [print(key,':', val) for key, val in metrices.items()]
            if self.online_run:
                [self.run.log(f"{key}:", val) for key, val in metrices.items()]
        else:
            raise AssertionError("Please first have predictions to check scoring metrics!")
    
    def classification_confusion_matrix(self, name=""):
        """ confusion matrix of the classification 
        """
        if hasattr(self, 'pred_test'): 
            labels = [(int(i)) for i in sorted(self.y.unique().tolist())]
            apply_confusion_matrix(self.y, self.pred_test, labels, self.online_run, name)
        else:
            raise AssertionError("Please first train a model and do predictions!")
            

def apply_confusion_matrix(y_test, pred_test, labels, online_run, name):
    """ confusion matrix of the classification 
    """
    cf_matrix = confusion_matrix(y_test, pred_test, labels=labels)
    cf_matrix_percentage = cf_matrix.astype('float') / cf_matrix.sum(axis=1)[:, np.newaxis]            
    sns.set(rc={'figure.figsize':(10, 18)})
    fig, axs = plt.subplots(nrows=2)
    fig.suptitle(f"Confusion Matrix", fontsize=20)
    g1 = sns.heatmap(cf_matrix, annot=True, fmt='g', cmap='Blues', ax=axs[0])
    g2 = sns.heatmap(cf_matrix_percentage, annot=True, fmt='.1%', cmap='Blues', ax=axs[1])
    g1.set_xlabel('Predicted Values')
    g1.set_ylabel('Actual Values ')
    g1.xaxis.set_ticklabels(labels)
    g1.yaxis.set_ticklabels(labels)
    g2.set_xlabel('Predicted Values')
    g2.set_ylabel('Actual Values ')
    g2.xaxis.set_ticklabels(labels)
    g2.yaxis.set_ticklabels(labels)
    plt.show()
    if online_run:
        # save figure
        filename=f'./outputs/confusion_matrix_{name}.png'
        plt.savefig(filename, dpi=600)
        plt.close()
    
def set_interval(x):
    """ evaluation intervals of the ratio between
        two continious features
    """
    if (x >= 0.9) & (x <= 1.11):
        value = "very_high"
    if (x < 0.9) | (x > 1.11):
        value = "high"
    if (x < 0.8) | (x > 1.25):
        value = "medium"
    if (x < 0.7) | (x > 1.43):
        value = "low"
    if (x < 0.5) | (x > 2):
        value = "very_low"
    return value

def apply_regression_metrics(y_test, pred_test):
    """ show metrics for selected two continuous columns to be
        compared with each other 
    """   
    metrices = {
        'MAE': mean_absolute_error(y_test, pred_test),
        'RMSE': mean_squared_error(y_test, pred_test, squared=False),
        'R2': r2_score(y_test, pred_test),
        'LOG': np.sqrt(mean_squared_log_error(y_test, pred_test)),
        'MAPE': mean_absolute_percentage_error(y_test, pred_test),
        'samples_test': len(y_test),    
    }
    return metrices

def apply_classification_metrics(y_test, pred_test):
    """ show relevant classification score metrics for the test data
    """  
    metrices = {
        'mean_relative_error': round(mean_relative_error(y_test, pred_test), 3),
        'mean_abs_error': round(mean_abs_error(y_test, pred_test), 3),
        'accuracy':  round(accuracy_score(y_test, pred_test), 3),
        'precision': round(precision_score(y_test, pred_test, average="weighted"), 3),
        'recall':    round(recall_score(y_test, pred_test, average="weighted"), 3),
        'f1_value':  round(f1_score(y_test, pred_test, average="weighted"), 3),
        'samples_test': len(y_test),    
    }
    return metrices

def mean_relative_error(y_true, y_pred, drop_inf=True):
    re = np.abs(y_true - y_pred)/y_true
    if drop_inf:
        mre = np.sum(re[re != np.inf])/len(re[re != np.inf])
    else:
        mre = np.sum(re)/len(re)
    return mre

def mean_abs_error(y_true, y_pred):
    return np.sum(np.abs(y_true - y_pred))/len(y_true)

def accuracy_score(y_true, y_pred):
    return sum(y_pred==y_true)/len(y_true)