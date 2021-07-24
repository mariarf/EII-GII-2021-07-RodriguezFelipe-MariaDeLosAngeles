import pandas as pd
from sodapy import Socrata
import os

class HistoricalApiTraffic:
    # Fecha y hora tienen que estar en formato: yyyy-mm-ddThh:mm:ss
    def traffic_historical(self, datalimit, start_datetime, end_datetime):


        client = Socrata("data.cityofnewyork.us", None)

        # Primeros resultados de dataLimit, devueltos como JSON desde la API / convertidos
        # a una lista de Python de diccionarios de sodapy.
        date = f"data_as_of between '{start_datetime}' and '{end_datetime}'"
        print(date)
        
        columns = "data_as_of, speed, travel_time, link_name"

        results = client.get("i4gi-tjb9", limit = datalimit, borough = "Manhattan", where = date, select = columns)
        
        # Conversión de datos a pandas DataFrame
        results_df = pd.DataFrame.from_records(results)
    
        # Conversión de datos de fecha y hora 
        #----------------------------------------- datetime - time_hour --------------------------------------#
        results_df["datetime"] = results_df["data_as_of"].str[:-9] + "00:00"
        results_df["datetime_traffic"] = results_df["data_as_of"].str[:-4]
        
        results_df["datetime"] = pd.to_datetime(results_df["datetime"])
        results_df["datetime_traffic"] = pd.to_datetime(results_df["datetime_traffic"])
        results_df["weekday"] = results_df['datetime'].dt.day_name()

        results_df = results_df[["datetime", "datetime_traffic", "weekday", "speed", "travel_time", "link_name"]]
    
        file_name = os.getcwd() + f"/apis/historical_apis/out_historical_apis/historical/traffic_historical/traffic_historical_{start_datetime[0:13]}_to_{end_datetime[0:13]}.csv"

        results_df.to_csv(file_name, index=False)
        print(f"HistoricalApiTraffic: {file_name}")





