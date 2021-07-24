import pandas as pd
import json, os, urllib3, certifi
from utils_historical_apis import UtilsHistoricalApis 

class HistoricalApiAirQuality:
    # Método que se conecta con la api y guarda datos en un rango de fecha  
    def air_quality_historical(self, start_datetime, end_datetime):
        
        # archivo donde se guardan los datos
        file_name = os.getcwd() + f"/apis/historical_apis/out_historical_apis/historical/air_quality_historical/air_quality_historical_{start_datetime[0:13]}_to_{end_datetime[0:13]}.csv"
    
        # pasando hora de NY a UTC para hacer la solicitud a la hora deseada
        utils = UtilsHistoricalApis()
        str_ny = utils.get_str_ny()
        start_datetime = utils.convert_time_str(start_datetime, str_ny, 'UTC')[0:13]
        end_datetime = utils.convert_time_str(end_datetime, str_ny, 'UTC')[0:13]
        
        # manejo de la verificación de certificados y las advertencias SSL
        # https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

        # obtener los datos desde la API
        url = f"https://www.airnowapi.org/aq/data/?startDate={start_datetime}&endDate={end_datetime}&parameters=OZONE,PM25&BBOX=-74.025831,40.700063,-73.911848,40.876821&dataType=A&format=application/json&verbose=1&nowcastonly=0&includerawconcentrations=0&API_KEY=3085AC4D-D4B0-4876-BF8F-FFE541AC6932"
        response = http.request('GET', url)
        
        # decodificar datos json en un objeto dict
        data = json.loads(response.data.decode('utf-8'))
        results_df = pd.DataFrame(data)

        results_df= results_df.drop(results_df[results_df['SiteName'] != 'CCNY'].index)
        results_df = results_df.rename(columns={"UTC": "datetime"}) 
        results_df["datetime"] = pd.to_datetime(results_df["datetime"])
        results_df = results_df[["datetime", "AQI", "Parameter"]]

        results_df["datetime"] = results_df["datetime"].dt.tz_localize('UTC').dt.tz_convert(str_ny).dt.strftime("%Y-%m-%dT%H:%M:%S")

        pm25_df = results_df.drop(results_df[results_df['Parameter']=="OZONE"].index)
        ozone_df = results_df.drop(results_df[results_df['Parameter']=="PM2.5"].index)

        # se guardan los valores en una sola fila por hora
        air_quality_df = pd.merge(pm25_df, ozone_df, on = "datetime", how = "outer", suffixes= ("_PM2.5", "_OZONE"))
        # aseguramos guardar valor en orden de fecha
        air_quality_df.drop(['Parameter_PM2.5', 'Parameter_OZONE'], axis=1, inplace=True)
        air_quality_df = air_quality_df.sort_values("datetime")

        # se guardan los datos en un csv
        air_quality_df.to_csv(file_name, index=False)

        print(f"HistoricalApiAirQuality: {file_name}")