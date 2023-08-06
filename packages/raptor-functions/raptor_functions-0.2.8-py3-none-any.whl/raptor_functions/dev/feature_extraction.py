

from scipy.signal import find_peaks
from scipy import stats
import pandas as pd
import numpy as np
import xgboost as xgb
from boruta import BorutaPy
from tsfresh.utilities.dataframe_functions import impute
from tsfresh.feature_extraction import ComprehensiveFCParameters
from tsfresh import extract_features, extract_relevant_features, select_features





FEATURES = [ 'exp_unique_id', 'timesteps', 'sensor_1', 'sensor_2',
       'sensor_3', 'sensor_4', 'sensor_5', 'sensor_6', 'sensor_7', 'sensor_8',
       'sensor_9', 'sensor_10', 'sensor_11', 'sensor_12', 'sensor_13',
       'sensor_14', 'sensor_15', 'sensor_16', 'sensor_17', 'sensor_18',
       'sensor_19', 'sensor_20', 'sensor_21', 'sensor_22', 'sensor_23',
       'sensor_24', 'result']

extraction_settings = ComprehensiveFCParameters()


def get_features(df, unique_id='exp_unique_id', label='result', timesteps='timesteps', features=FEATURES):


    df = df[FEATURES]

    X = df.drop(label, axis=1)
    y = df.groupby(unique_id).first()[label]

    X = extract_features(X, column_id=unique_id, column_sort=timesteps,
                     default_fc_parameters=extraction_settings,
                     
                     # we impute = remove all NaN features automatically
                     impute_function=impute)



    return X, y

    

forest = xgb.XGBClassifier()
boruta = BorutaPy(
estimator = forest, 
n_estimators = 'auto',
max_iter = 100 # number of trials to perform
)

def get_relevant_features(X, y):

    ### fit Boruta (it accepts np.array, not pd.DataFrame)
    boruta.fit(np.array(X), np.array(y))
    
    
    ### print results
    green_area = X.columns[boruta.support_].to_list()
    blue_area = X.columns[boruta.support_weak_].to_list()

    relevant_features = green_area + blue_area
    X_f = X[relevant_features]
    dff = X_f.join(y)

    dff.columns = dff.columns.str.replace('[",\d, (, )]', '')

    return dff, relevant_features
