
import joblib
from io import BytesIO
import boto3
from tsfresh.feature_extraction import settings, extract_features








def load_model(path):
    ''' 
       Function to load a joblib file from an s3 bucket or local directory.
       Arguments:
       * path: an s3 bucket or local directory path where the file is stored
       Outputs:
       * file: Joblib file loaded
    '''

    # Path is an s3 bucket
    if path[:5] == 's3://':
        s3_bucket, s3_key = path.split('/')[2], path.split('/')[3:]
        s3_key = '/'.join(s3_key)
        with BytesIO() as f:
            boto3.client("s3").download_fileobj(Bucket=s3_bucket, Key=s3_key, Fileobj=f)
            f.seek(0)
            file = joblib.load(f)
    
    # Path is a local directory 
    else:
        with open(path, 'rb') as f:
            file = joblib.load(f)
    
    return file













def get_prediction_features(df, relevant_features, id='exp_unique_id', timesteps='timesteps'):

    fc_parameters = settings.from_columns(relevant_features)

    prediction_data = extract_features(df, kind_to_fc_parameters =fc_parameters, column_id=id, column_sort=timesteps)

    prediction_data.columns = prediction_data.columns.str.replace('["]', '')

    return prediction_data






# def random_sample(df_list,x_columns):
#   i = random.randint(0, len(df_list))
#   df_temp = df_list[i]
#   df_temp = df_temp[x_columns]
#   # df_temp = df_temp.iloc[:,[1,2,3,4,5,6,7,8,9,10,11,12]]
#   j = random.randint(0, len(df_temp.count()))
#   input_data_sample = df_temp.iloc[[j]]
#   print(input_data_sample)
#   # 
#   x = input_data_sample.columns.tolist()
#   y = input_data_sample.iloc[0].values.tolist()
#   # 
#   plt.bar(x, y)
#   fig = plt.gcf()
#   fig.autofmt_xdate()
#   # 
#   return input_data_sample

# def sample_prediction(input_data_sample, model):
#   # 
#   print('Prediction: ' + str(model.predict(input_data_sample)))
#   print('Prediction Probability: ' + str(model.predict_proba(input_data_sample)))