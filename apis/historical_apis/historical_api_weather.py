import pandas as pd
import os, requests, io

class HistoricalApiWeather:
    # Método que se conecta con la api y guarda datos en un rango de fecha en NY time
    def weather_historical(self, start_datetime, end_datetime):

        start_datetime= start_datetime[0:-5] + "00:00"

        # API
        url = "https://visual-crossing-weather.p.rapidapi.com/history"
        querystring = {"startDateTime":f"{start_datetime}","aggregateHours":"1","location":"Manhattan,NY,USA","endDateTime":f"{end_datetime}","unitGroup":"us","dayStartTime":"0:00:00","contentType":"csv","dayEndTime":"23:59:59","shortColumnNames":"0"}

        # la API key puede hacer 500 solicitudes por mes, en caso de necesitar más pedir key nueva en rapidApi
        headers = {
            'x-rapidapi-key': "91fe12497fmshec2c60cb1d22778p1da8d8jsnd536d7b3c9b9",
            'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
            }
        response = requests.request("GET",url, headers=headers, params = querystring)  
        results_df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        
        # tipografía de los datos 
        results_df["Date time"] = pd.to_datetime(results_df["Date time"]).dt.strftime("%Y-%m-%dT%H:%M:%S")
        results_df = results_df.rename(columns={"Date time": "datetime"}) 
        results_df = results_df.drop(["Address","Latitude","Longitude","Resolved Address","Name","Info", "Weather Type", 'Heat Index', 'Wind Gust', 'Wind Chill'], axis=1)

        results_df["Conditions"]= results_df["Conditions"].str.replace(",", "")

        # guardando los datos en CSV
        file_name = os.getcwd() + f"/apis/historical_apis/out_historical_apis/historical/weather_historical/weather_historical_{start_datetime[0:13]}_to_{end_datetime[0:13]}.csv"
        results_df.to_csv(file_name, index=False)

        print(f"HistoricalApiWeather: {file_name}")