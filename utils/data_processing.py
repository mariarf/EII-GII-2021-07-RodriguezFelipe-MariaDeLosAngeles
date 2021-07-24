import pandas as pd
import os
import numpy as np
from utils.predictions_processing import PredictionsProcessing

class DataProcessing:

    def __init__(self):
        print('·-'*60)
        print("DataProcessing: _init_")
        print('·-'*60)
        train_df = pd.read_csv(os.getcwd() + "/in/normalize_data/train_data.csv",  low_memory=False)
        self.train_mean = train_df.mean()
        self.train_std = train_df.std()

    # Método que ordena las columnas y sus contenidos para que sea compatible con el modelo
    # registra el valor verdadero para el AQI en ./out/predictions
    def data_preprocessing(self, file_path, hour_datetime):
        df = pd.read_csv(file_path)
        df = df.fillna(0)

        df.drop(['datetime_traffic', 'link_name', 'Precipitation Cover'], axis=1, inplace=True) 
     
        df['weekday'] = df['weekday'].replace(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday' ],['1','2','3','4','5','6','7'])
        df['weekday'] = df['weekday'].astype(np.float32)

        df['Conditions'] = df['Conditions'].astype('category')
        df['Conditions'] = df['Conditions'].cat.codes
        df['Conditions'] = df['Conditions'].astype(np.float32)

        df.insert(0, 'AQI', df[['AQI_PM2.5','AQI_OZONE']].max(axis=1))

        df.drop(['AQI_PM2.5','AQI_OZONE'], axis=1, inplace=True)
        df = df.groupby('datetime').mean()

        # Conversión a radianes
        wd_rad = df.pop('Wind Direction')*np.pi / 180
        wv = df.pop('Wind Speed')

        # Calculo de las componentes x e y del viento
        df['Wx'] = wv*np.cos(wd_rad)
        df['Wy'] = wv*np.sin(wd_rad)
        
        df['datetime'] = df.index
        df.reset_index(drop=True, inplace=True)
        
        date_time = pd.to_datetime(df.pop('datetime'), format='%Y-%m-%dT%H:%M:%S')
        timestamp_s = date_time.map(pd.Timestamp.timestamp)

        day = 24*60*60
        year = (365.2425)*day

        df['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
        df['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
        df['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
        df['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))

        # Se registra el verdadero valor del AQI
        value = df.loc[0,"AQI"]
        PredictionsProcessing().add_value(hour_datetime, False, value)

        file_path = os.getcwd() + f"/in/group_data_by_datetime.csv"
        df.to_csv(file_path, index=False)
        self.normalize_data()

    # Método que guarda los valores de ./in/group_data_by_datetime.csv 
    # normalizados en el archivo ./in/normalize_data/normal_data.csv
    def normalize_data(self):
        file_path = os.getcwd() + f"/in/group_data_by_datetime.csv"
        df = pd.read_csv(file_path)

        df = (df - self.train_mean) / self.train_std

        file_path = os.getcwd() + f"/in/normalize_data/normal_data.csv"
        df_normal = pd.read_csv(file_path, low_memory=False)
        df_normal = pd.concat([df_normal, df])
        df_normal.to_csv(file_path, index=False)
        
    # Dado un valor y la columna a la que pertenece desnormaliza el valor    
    def denormalize_data(self, num, pos):
        value = (num * self.train_std[pos]) + self.train_mean[pos]
        return round(value, 1)