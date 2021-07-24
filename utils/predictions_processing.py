import pandas as pd
import os

class PredictionsProcessing:

    def __init__(self):
        self.path = os.getcwd() + "/out/predictions/predictions.csv"

    
    # Método que añade los nuevos valores del AQI al archivo ./out/predictions/predictions.csv
    def add_value(self, hour_datetime, prediction, value, t=0):
        df= pd.read_csv(self.path)
        hour_datetime_ = str(hour_datetime)

        if not df.datetime.isin([hour_datetime_]).any().any():
            df = df.append({'datetime':hour_datetime_}, ignore_index=True)
        
        cat = self.set_category(value)

        if prediction:
            print("add prediction:", hour_datetime)
            df.loc[df.datetime == hour_datetime_, f"predict_aqi_t{t}"] = value
            df.loc[df.datetime == hour_datetime_, f"predict_category_t{t}"] =  cat[0]
            df.loc[df.datetime == hour_datetime_, f"predict_color_t{t}"] =  cat[1]
        else:     
            print("add real:", hour_datetime)
            df.loc[df.datetime == hour_datetime_, "real_aqi"] = value
            df.loc[df.datetime == hour_datetime_, "real_category"] = cat[0]
            df.loc[df.datetime == hour_datetime_, "real_color"] = cat[1]
        
        df.to_csv(self.path, index=False)


    def add_real(self, hour_datetime, value):
        df= pd.read_csv(self.path)
        hour_datetime_ = str(hour_datetime)
        print("add real:", hour_datetime)
        
        if not df.datetime.isin([hour_datetime_]).any().any():
            df = df.append({'datetime':hour_datetime_}, ignore_index=True)
            
        cat = self.set_category(value)

        df.loc[df.datetime == hour_datetime_, "real_aqi"] = value
        df.loc[df.datetime == hour_datetime_, "real_category"] = cat[0]
        df.loc[df.datetime == hour_datetime_, "real_color"] = cat[1]
        df.to_csv(self.path, index=False)

    def add_prediction(self, hour_datetime, value, t):
        df= pd.read_csv(self.path)
        hour_datetime_ = str(hour_datetime)
        print("add prediciton t:", t, hour_datetime)

        if not df.datetime.isin([hour_datetime_]).any().any():
            df = df.append({'datetime':hour_datetime_}, ignore_index=True)

        cat = self.set_category(value)
        
        df.loc[df.datetime == hour_datetime_, f"predict_aqi_t{t}"] = value
        df.loc[df.datetime == hour_datetime_, f"predict_category_t{t}"] =  cat[0]
        df.loc[df.datetime == hour_datetime_, f"predict_color_t{t}"] =  cat[1]
        df.to_csv(self.path, index=False)
    
    # Método que de acuerdo con el AQI devuelve la categoría y el color correspondiente
    def set_category(self, value):
        if value <= 50:
            return ["Buena", "rgb(168, 224, 95)"]
        elif value > 50 and value <= 100:
            return ["Moderada", "rgb(253,215,77)"]
        elif value > 100 and value <= 150:
            return ["Dañina a la Salud de los Grupos Sensibles", "rgb(254,156,89)"]
        elif value > 151 and value <= 200:
            return ["Dañina a la Salud", "rgb(254,108,107)"]
        elif value > 201 and value <= 300:
            return ["Muy Dañina a la Salud", "rgb(118, 44, 168)"]
        elif value > 300:
            return ["Arriesgado", "rgb(129, 43, 31)"]    