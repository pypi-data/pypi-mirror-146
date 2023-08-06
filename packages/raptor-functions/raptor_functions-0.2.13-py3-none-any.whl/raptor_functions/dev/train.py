# Importing the Packages:
import optuna
import pandas as pd
import mlflow
import os

try:
    from sklearn.utils import safe_indexing
except ImportError:
    from sklearn.utils import _safe_indexing

    
from pycaret.classification import *
import numpy as np
import pandas as pd
from sklearn.metrics import recall_score





SENSORS_FEATURES = ['sensor_1','sensor_2','sensor_3','sensor_4','sensor_5',
 'sensor_6', 'sensor_7', 'sensor_8', 'sensor_9', 'sensor_10', 'sensor_11', 'sensor_12', 'sensor_13',
 'sensor_14', 'sensor_15', 'sensor_16', 'sensor_17', 'sensor_18', 'sensor_19', 'sensor_20', 'sensor_21', 'sensor_22', 'sensor_23', 'sensor_24']

STAGES = ['baseline', 'absorb', 'pause', 'desorb', 'flush']
TARGET_COL = 'result'

# artifact_path = 's3://raptor-mlflow-data/mlartifacts/1/83318437749c4e59a4950f55a98b2ad6/artifacts'
# artifact_path = 's3://raptor-mlflow-data'


def get_plots(model):

    model_attributes = dir(model)

    plot_model(model, plot = 'confusion_matrix', save=True)
    cm = os.path.join(os.getcwd(), 'Confusion Matrix.png')
    mlflow.log_artifact(cm)
    # log_artifact(cm)

    plot_model(model, plot = 'class_report', save=True) 
    cr = os.path.join(os.getcwd(), 'Class Report.png')
    mlflow.log_artifact(cr)  
    # log_artifact(cr)
    


    if 'predict_proba' in model_attributes:
        try:
            plot_model(model, plot = 'auc', save=True)
            auc = os.path.join(os.getcwd(), 'AUC.png')
            mlflow.log_artifact(auc) 

            plot_model(model, plot = 'pr', save=True) 
            pr = os.path.join(os.getcwd(), 'Precision Recall.png')
            mlflow.log_artifact(pr)

            plot_model(model, plot = 'calibration', save=True) 
            cc = os.path.join(os.getcwd(), 'Calibration Curve.png')
            mlflow.log_artifact(cc)
        except:
            pass
  

    
    if 'feature_importances_' in model_attributes:  
        plot_model(model, plot = 'feature', save=True)  
        fi = os.path.join(os.getcwd(), 'Feature Importance.png')
        mlflow.log_artifact(fi)





def specificity(actual, pred, pos_label=0):
    return recall_score(actual, pred, pos_label=pos_label)





def objective(trial, df, study_name, model_mode):

        mlflow.set_experiment(study_name)

       
        mlflow.set_tracking_uri(
            # "http://ec2-3-10-175-206.eu-west-2.compute.amazonaws.com:5000/"
            'http://ec2-3-10-210-150.eu-west-2.compute.amazonaws.com:5000/'
            )
        

        mlflow.start_run()


        features = df.drop('result', axis=1)
        clf = setup(df, target = 'result', silent=True, log_plots=True, experiment_name=study_name, preprocess=False)

        add_metric('specificity', 'Specificity', specificity)
        remove_metric('MCC')
        remove_metric('Kappa')

        MODELS = dict(models()['Name'])


        if model_mode == 'random':

            model_id = trial.suggest_categorical("model", list(MODELS.keys()))
            model_name = MODELS[model_id]
            model = create_model(model_id)
            predict_model(model)
            metrics = pull().iloc[:,1:]
            keys = metrics.columns
            values = metrics.values[0]
            metrics = dict(zip(keys, values))


            get_plots(model)
            mlflow.sklearn.log_model(model, artifact_path=model_name)
           
        # elif model_mode == 'xgb':

        #     model = create_model('xgb')
        #     predict_model(model)
        #     metrics = pull().iloc[:,1:]
        #     keys = metrics.columns
        #     values = metrics.values[0]
        #     metrics = dict(zip(keys, values))
            

        #     get_plots(model)
        #     mlflow.sklearn.log_model(model, artifact_path=model_name)
                    
        else:

            model = compare_models()

            model_name = model.__class__.__name__
            predict_model(model)
            metrics = pull().iloc[:,1:]
            keys = metrics.columns
            values = metrics.values[0]
            metrics = dict(zip(keys, values))


            get_plots(model)
            mlflow.sklearn.log_model(model, artifact_path=model_name)

            


            
        model_params = model.get_params()
        


        mlflow.log_metrics(metrics)

        try:
            mlflow.set_tag('sensor_cols', features)
  
        except:
            pass

        mlflow.set_tag('model_name', model_name)
        mlflow.set_tag('model_params', model_params)
        
        mlflow.set_tag('model_mode', model_mode)

        mlflow.end_run()







def train_experiments(df, study_name='raptor', direction='maximize', model_mode='random', n_trials=5):
    """trains several models during different trials and logs them. Experiemnt can be tracked on "http://ec2-3-10-175-206.eu-west-2.compute.amazonaws.com:5000/"


    Args:
        df (pandas dataframe): dataframe of cyclic sensor data to be used for training
        study_name (str, optional): optuna study name to use. Defaults to 'raptor'.
        direction (str, optional): dirtection of objective. Defaults to 'maximize'.
        stage (str or list, optional): Can take any of ('baseline', 'absorb', 'pause', 'desorb', 'flush') as a str or combination as a list. 
                                        Can also take str 'all' for all stages and 'random' for random stage or stages. Defaults to 'pause'.        sensor (str, optional): _description_. Defaults to '12'.
        use_average (bool, optional): if True, uses average of stages selected. Defaults to False.
        model_mode (str, optional): _description_. Defaults to 'random'.
        n_trials (int, optional): number of times to run experiments. Defaults to 5.
        suggest (bool, optional): if True, suggest features, stage, model mode to use for training. Defaults to False.
    """    
    
    

    study = optuna.create_study(study_name=study_name, direction=direction)
    study.optimize(lambda trial: objective(trial, df, study_name, model_mode), n_trials=n_trials)

    print('Click on this link to track experiments: ', 
    # "http://ec2-3-10-175-206.eu-west-2.compute.amazonaws.com:5000/"
    'http://ec2-3-10-210-150.eu-west-2.compute.amazonaws.com:5000/'
    )
