from historical_api_traffic import HistoricalApiTraffic
from historical_api_air_quality import HistoricalApiAirQuality
from historical_api_weather import HistoricalApiWeather
import os, datetime, calendar
import pandas as pd
from datetime import datetime as dt

# Método que dada una fecha de inicio, un número de meses y un directorio recoge los datos
# a partir de la fecha de inicio durante el número de meses que se le indica
###### La fecha de inicio debe ser mes y año yyyy-mm.
def apis_request(start_date, months, directory):
    start_date = start_date + "01T00:00:00"

    start_datetime = datetime.datetime.strptime(start_date,"%Y-%m-%dT%H:%M:%S")
    end_datetime = start_datetime + datetime.timedelta(days=14, hours= 23, seconds=3599)
    end_datetime = str(end_datetime).replace(" ","T")
    start_datetime = str(start_datetime).replace(" ","T")
    print(end_datetime[0:19])

    path_file = os.getcwd() + '\\apis\\historical_apis\\out_historical_apis\\merge_historical\\' + directory

    while os.path.exists(path_file):
        print("Select another name for the folder")
        directory= input()
        path_file = os.getcwd() + '\\apis\\historical_apis\\out_historical_apis\\merge_historical\\' + directory
    
    print("Folder: ", path_file)
    os.mkdir(path_file)

    output_name = f"\\historical_data_{directory}.csv"
    print(path_file)

    count = 0
    num = months*2
    while count < num:  

        HistoricalApiTraffic().traffic_historical(10000000, start_datetime, end_datetime)
        HistoricalApiAirQuality().air_quality_historical(start_datetime, end_datetime)
        HistoricalApiWeather().weather_historical(start_datetime, end_datetime)
        res = start_datetime[0:13] + "_to_" + end_datetime[0:13]
        merge_by_datetime(path_file, res)

        start_datetime = dt.strptime(str(end_datetime), "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(seconds = 1)
      
        if start_datetime.day == 1:
            plus = 14
        else:
            res = calendar.monthrange(start_datetime.year, start_datetime.month)
            plus = res[1] - 16
      
        end_datetime =  start_datetime + datetime.timedelta(days=plus, hours= 23, seconds=3599)

        start_datetime = str(start_datetime).replace(" ","T")
        end_datetime = str(end_datetime).replace(" ","T")
        count += 1

    merge_files_with_location(path_file, output_name)

def merge_by_datetime(path_file, datetime):

    data_folder = os.getcwd() + "/apis/historical_apis/out_historical_apis/historical"

    traffic_file = data_folder + f"/traffic_historical/traffic_historical_{datetime}.csv"
    airQuality_file = data_folder + f"/air_quality_historical/air_quality_historical_{datetime}.csv"
    weather_file = data_folder + f"/weather_historical/weather_historical_{datetime}.csv"
    print(path_file)
    pepe = f"/merge_{datetime}.csv"
    print(pepe)
    file_name = path_file + f"/merge_{datetime}.csv"

    traffic_df = pd.read_csv(traffic_file)
    airQuality_df = pd.read_csv(airQuality_file)
    weather_df = pd.read_csv(weather_file)

    traffic_df["datetime"] = pd.to_datetime(traffic_df["datetime"])
    airQuality_df["datetime"] = pd.to_datetime(airQuality_df["datetime"])
    weather_df["datetime"] = pd.to_datetime(weather_df["datetime"])
   
    df = pd.merge(traffic_df,airQuality_df, how= 'outer', on = 'datetime', suffixes= ('_TRAFFIC', '_AIR'))
    df = pd.merge(df, weather_df, how="outer", on="datetime", suffixes= ('','_WEATHER'))
    
    df = df.sort_values("datetime_traffic")

    df.to_csv(file_name,index=False)

    print(f"Merge - Traffic, Air Quality, Weather: {file_name}")
  

def merge_files_with_location(location, output_name):

    path = location #path to merge files
    dirs = os.listdir(path) #files in that directory
    df = pd.DataFrame()
   
    # Nombre de carpetas/archivos contenidos en la ubicación desde la que queremos fusionar los archivos. 
    # De esta forma, no se tendrán en cuenta al fusionar todos los archivos.
    undesired_paths = [""]
    
    for file in dirs:
        if file in undesired_paths:
            continue # no se añade el archivo
        else:
            file = path +"\\" + file # se itera en todos los archivos
            df_concat = pd.read_csv(file, low_memory=False) # archivo donde se concadenan los datos
            df = pd.concat([df,df_concat]) 
            print("write: " + file) 

    print(df.shape[0]) 

    # se guarda el archivo con el nombre indicado
  
    output_csv =  location + output_name
    df.to_csv(output_csv, index=False)

#apis_request("yyyy-mm", number_of_month, "file_name")
