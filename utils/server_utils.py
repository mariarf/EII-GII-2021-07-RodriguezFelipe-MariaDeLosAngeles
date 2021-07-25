import pytz, datetime, os
import pandas as pd

class ServerUtils:
    def __init__(self):
        self.tz_NY = pytz.timezone('America/New_York')
        self.path_merge = os.getcwd() + '/out/predictions/predictions.csv'
    
    def datetime_ny(self):
        
        datetime_NY = datetime.datetime.now(self.tz_NY)
        date =  datetime_NY.strftime("%Y-%m-%d %H:%M:%S")
        date_hour = date[:-5] + "00:00"
        return date, date_hour 

    def get_basic_data(self):
        
        predictions = pd.read_csv(self.path_merge)

        date, date_hour = self.datetime_ny()

        if not predictions.isin(predictions.loc[predictions.datetime == date_hour]).any().any():
            actual_aqi = predictions.tail(1)
        else:
            actual_aqi = predictions.loc[predictions.datetime == date_hour]
        
        actual_aqi = actual_aqi.to_numpy().tolist()
        return date, actual_aqi

    def get_predict_t(self, tail_num, t):

        predictions = pd.read_csv(self.path_merge)
        pred = pd.DataFrame()
        if len(predictions) < 19:
            return pred
        predictions = predictions[16:]
        predictions = predictions.tail(tail_num) 

        pred = predictions[['datetime', f'predict_aqi_t{t}', f'predict_category_t{t}', f'predict_color_t{t}', 'real_aqi', 'real_category', 'real_color']]
        
        pred = pred.loc[~pred[f'predict_aqi_t{t}'].isnull()]

        pred = pred.rename(columns={f'predict_aqi_t{t}': "predict_aqi", f'predict_category_t{t}': 'predict_category', f'predict_color_t{t}': 'predict_color'}) 
        
        pred['error'] = ''
        pred['predict_bg_color'] = pred['predict_color']
        pred['real_bg_color'] = pred['real_color'].str.replace(')', ",0.2)")
        pred['error'] = pred[f'predict_aqi'] - pred[f'real_aqi']

        pred[:-3]=pred[:-3].fillna(method="bfill")


        return pred
    