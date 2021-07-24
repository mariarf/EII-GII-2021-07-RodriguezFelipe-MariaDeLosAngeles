import pandas as pd
import requests, io
from datetime import datetime as dt
from datetime import timedelta as timedelta
from apis.utils_realtime_apis import UtilsRealtimeApis

class ApiWeather:
    # Método que se conecta con la api y guarda datos para la hora dada
    def weather_data_ingestion(self, start_datetime, file_dir):
        utils = UtilsRealtimeApis()
        datetime= start_datetime[0:-5] + "00:00"

         # la API key puede hacer 500 solicitudes por mes, en caso de necesitar más pedir key nueva en rapidApi
        if int(datetime[8:10]) < 15:
            key = "734d8fc071msh3aec09695fe1d3cp1bc2c8jsn62efb25c06b7"

        else:
            key= "5bbbe8b746msh1b66cc8a070eee3p10e005jsn7996bb65c02c"
        
        url = "https://visual-crossing-weather.p.rapidapi.com/history"
        querystring = {"startDateTime":f"{datetime}","aggregateHours":"1","location":"Manhattan,NY,USA","unitGroup":"us","dayStartTime":"0:00:00","contentType":"csv","dayEndTime":"23:59:59","shortColumnNames":"0"}

        headers = {
            'x-rapidapi-key': key,
            'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
            }
        response = requests.request("GET",url, headers=headers, params = querystring)  
    
        results_df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))

        res = utils.difference_datetime(start_datetime)
        date_format = utils.get_format_datetime()

        if results_df.empty or str(results_df.loc[0,"Info"]) == "No data available":
            #si han pasado mas de 3 horas (10800seg) y sigue estando vacio se pasa a la se consulta para la hora anterior
            if res.seconds > 10800:

                start_ = dt.strptime(start_datetime, date_format)  - timedelta(hours=1)
                print(start_)
                ApiWeather().weather_data_ingestion(str(start_).replace(" ", "T"), file_dir)
                
                result= pd.read_csv(file_dir)
                result["datetime"] = pd.to_datetime(result["datetime"])
                result.loc[0,"datetime"] = result.loc[0,"datetime"] + timedelta(hours=1)
                result["datetime"] =  result["datetime"].dt.strftime(date_format)
                result.to_csv(file_dir, index = False)
                
                print(f"WeatherApi.empty: {start_datetime}")
                return True
            return False
        
        #tipografia de los datos
        str_datetime = "Date time"
        results_df[str_datetime] = pd.to_datetime(results_df[str_datetime]).dt.strftime(date_format)
        results_df = results_df.rename(columns={str_datetime: "datetime"}) 
        results_df = results_df.drop(["Address","Latitude","Longitude","Resolved Address","Name","Info", 
                                        "Weather Type", 'Heat Index', 'Wind Gust', 'Wind Chill'], axis=1)
        
        results_df["Conditions"]= results_df["Conditions"].str.replace(",", "")

        #guardando datos obtenidos en csv 
        results_df.to_csv(file_dir, index=False)

        print(f"WeatherApi: {file_dir}")
        return True