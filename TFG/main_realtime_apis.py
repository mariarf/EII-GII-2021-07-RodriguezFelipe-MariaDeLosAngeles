from datetime import datetime as dt
from datetime import timedelta as timedelta

from apis.api_traffic import ApiTraffic
from apis.api_air_quality import ApiAirQuality
from apis.api_weather import ApiWeather
from apis.utils_realtime_apis import UtilsRealtimeApis
from utils.data_processing import DataProcessing
from utils.model import Model

import pandas as pd
import threading, time, os, pytz


class MainRealtimeApis:

    """ _init_
    Se registra la hora de ejecución
    Se guardan en variables las rutas de los archivos
    Se guardan en listas las cabeceras para cada archivo
    Se guarda el input_width, historic y out_steps que se utilizarán para cargar el histórico de datos
    """
    
    file = os.getcwd() + "\\apis\out_apis\merge.csv"
    def __init__(self, input_width, out_steps, historic=0):

        self.input_width = input_width
        self.out_steps = out_steps
        self.historic = historic

        self.utils = UtilsRealtimeApis()
        self.model = Model(input_width, out_steps)

        self.format_datetime = self.utils.get_format_datetime()
        tz_NY = pytz.timezone('America/New_York') 
        ini_datetime = dt.now(tz_NY).strftime(self.format_datetime)
        self.ini_datetime = ini_datetime[:-5] + "00:00"
        self.input_datetime = self.ini_datetime

        self.next_iter_air_quality = False
        self.next_iter_weather = False

        self.traffic_file, self.air_quality_file, self.weather_file, self.merge_file, self.normal_data_file, self.predict_data_file = self.utils.get_realtime_apis_file_directions()
        self.list_traffic, self.list_air_quality, self.list_weather, self.list_merge, self.list_normal_data, self.list_predict_data = self.utils.get_lists()
        self.traffic_iter_time = 5*60


    """ MÉTODOS PARA LLAMAR A LAS APIS
    """
    def traffic_api(self, iter_time, limit):
        print("traffic: executed")
        
        api_traffic = ApiTraffic()
        self.traffic_iter_time = iter_time
        """ 
            -- mientras el método de la API retorne falso se espera
            -- cuando el método de la API retorna verdadero se escribe el valor en merge y se empieza a iterar
        """  
        while not api_traffic.traffic_data_ingestion(limit, self.input_datetime, self.traffic_file):
            print("traffic: file not found - waiting to new values")
            time.sleep(iter_time)

        write_thread = threading.Thread(target=self.write, args = (self.traffic_file,) )
        write_thread.start()
        time.sleep(15)
        
        """ Se empieza a iterar
            -- los valores para la consulta a la api se toman del último valor registrado en el archivo merge
        """

        while True:
            traffic= pd.read_csv(self.merge_file)     #SE LEE EL ULTIMO REGISTRO DE FECHA REGISTRADO EN MERGE PARA TRÁFICO
            datetime = traffic.loc[traffic.index[-1], "datetime_traffic"]
            print("--"*50)
            print(f"traffic: call {datetime}")
            print("--"*50)
            
            while not api_traffic.traffic_data_ingestion(limit, datetime, self.traffic_file):
                print("traffic: WAITING TO NEW VALUES")
                time.sleep(iter_time)
            
            write_thread = threading.Thread(target=self.write, args = (self.traffic_file,) )
            write_thread.start()
            time.sleep(10)

    """ AirApi y Weather:
        Se consultan datos que se traen por hora
        --Al registrarlos en merge:
            * La fecha consultada debe ser menor que la fecha del último registro para tráfico en merge
            * Si se detecta un salto temporal en los datos de tráfico NO se introduce la línea con datos para aire y clima
            * APIS aire y clima - Si no hay valores para una Fecha y han pasado más de 2 horas se guarda el valor anterior

        --Se toma la hora de inicio y a medida que se rellenen los datos se le va sumando 1 hora

        --Recomendaciones: hacer iteraciones cada 30 minutos al menos. 
                        Las apis tardan entre 1 hora y 2 horas en devolver los datos deseados. 
                        Por lo que de esta forma si se consulta al pasar 1h de ejecución y la api 
                        genera el valor para cuando ha pasado 1h25min no se tiene que esperar 2h enteras.
    """
    def weather_api(self, iter_time):
        print("weather: executed")
        api_weather = ApiWeather()

        start_datetime = self.input_datetime

        while True:
            print("--"*50)
            print(f"weather: call {start_datetime}")
            print("--"*50)
            time.sleep(15)
            while not api_weather.weather_data_ingestion(start_datetime, self.weather_file):
                print(f"weather: WAITING TO NEW VALUES FOR WEATHER")
                time.sleep(iter_time)
            
            write_thread = threading.Thread(target=self.write, args = (self.weather_file, self.merge_file, self.list_weather) )
            write_thread.start()
            time.sleep(15)
        
            while not self.next_iter_weather:
                    print(f"weather: WAITING TO NEW VALUES FOR TRAFFIC {start_datetime}")
                    time.sleep(self.traffic_iter_time)
                    write_thread = threading.Thread(target=self.write, args = (self.weather_file, self.merge_file, self.list_weather) )
                    write_thread.start()
                    time.sleep(15)
            
            self.next_iter_weather = False
            start_datetime = dt.strptime(str(start_datetime), self.format_datetime) + timedelta(hours=1)
            start_datetime = str(start_datetime).replace(" ","T")

    def air_api(self, iter_time):
        print("air: executed")
        api_air_quality = ApiAirQuality()

        start_datetime = self.input_datetime

        while True:
            print("--"*50)
            print(f"air: call {start_datetime}")
            print("--"*50)
            time.sleep(20)
            while not api_air_quality.air_quality_data_ingestion(start_datetime, self.air_quality_file):
                print(f"air: WAITING TO NEW VALUES FOR air_quality")
                time.sleep(iter_time)
            
            write_thread = threading.Thread(target=self.write, args = (self.air_quality_file, self.merge_file, self.list_air_quality) )
            write_thread.start()
            time.sleep(20)
            while not self.next_iter_air_quality:
                    print(f"air: WAITING TO NEW VALUES FOR TRAFFIC {start_datetime}")
                    time.sleep(self.traffic_iter_time)
                    write_thread = threading.Thread(target=self.write, args = (self.air_quality_file, self.merge_file, self.list_air_quality) )
                    write_thread.start()
                    time.sleep(20)
            
            self.next_iter_air_quality = False
            start_datetime = dt.strptime(str(start_datetime), self.format_datetime) + timedelta(hours=1)
            start_datetime = str(start_datetime).replace(" ","T")


    """ write:
        *** recibe dos direcciones de archivos @file_name,  @merge_file_used y una lista @list con nombres de columnas
        - Si el @file_name es el correspondiente a tráfico
            *se registran los nuevos valores
        - Si el @file_name no es el de tráfico y @merge_file_used esta en blanco
            *se devuelve false y se sale del método
        - else
            *Se llama al método fileConcatMerge
                se devuelve el resultado de la llamada
                se registran los nuevos datos
        - Si se detecta que se han escrito los valores para el clima y el aire de la hora consultada
        se procesan los datos y se guardan normalizados
        - Si ya se cuenta con los suficientes datos de entrada para generar predicciones se hacen las predicciones
    """
    def write(self, file_name, merge_file_used=file, list=[]):
        print("write type:" + str(file_name))
       
        df0= pd.read_csv(merge_file_used)
        df0["datetime"] = pd.to_datetime(df0["datetime"])

        df1 = pd.read_csv(file_name)
        df1["datetime"] = pd.to_datetime(df1["datetime"]) 

        """ - SE REGISTRAN VALORES DE TRÁFICO
            - SI NO HAY VALORES DE TRÁFICO EN MERGE
                * se espera para guardar cualquier otro valor distinto a los de tráfico
        """   
        if file_name == self.traffic_file:
            df0 = pd.concat([df0, df1])
            df0.to_csv(merge_file_used, index= False)
            return
        elif df0.shape[0] <= 0:  #es decir aun no se guardan datos de tráfico
            return
            
        """ CONDICIÓN ^^Línea de arriba - if TRUE: FIN else FALSE: CONTINUE
            -- Si el documento no tiene ni un solo registro guardado no se ejecuta el resto del código
        """
        result = self.file_concat_merge(df0, df1, list)

        if file_name == self.air_quality_file:
            self.next_iter_air_quality = result[0] 

        elif file_name == self.weather_file:
            self.next_iter_weather= result[0]
        
        if not result[0]:
            return

        df0 = result[1]
        df0.to_csv(merge_file_used, index= False)
        print(result[2])

        hour_datetime = df1.loc[0, 'datetime']
        write_air = df0.loc[df0.datetime == hour_datetime, self.list_air_quality[1:]]
        write_weather = df0.loc[df0.datetime == hour_datetime, self.list_weather[1:]]
        if not write_air.isnull().all().all() and not write_weather.isnull().all().all():
            print("-*"*50)
            print(f"write - register: {hour_datetime}")
            print("-*"*50)
            df = df0.loc[df0.datetime == hour_datetime]
            file_path = os.getcwd() + "/apis/out_apis/merge_hour.csv"
            df.to_csv(file_path, index=False)
            DataProcessing().data_preprocessing(file_path, hour_datetime)
            
            if (hour_datetime + timedelta(hours=self.out_steps+self.historic+1)) >= dt.strptime(self.ini_datetime, "%Y-%m-%dT%H:%M:%S"):
                self.model.predict_results(hour_datetime)
        

    """ fileConcatMerge:   
        *** recibe dos dataframes @df0 y @df1 y una lista con nombres de columnas @columns
        -Incluye en @df0 los valores de @df1 de @columns cuando la columna "datetime" coincide
        -Sólo registra los valores de @df1 en @df0 
            *Si, se han recogido todos los valores de tráfico para el valor "datetime" en @df0
                es decir, se registra cuando el último valor de @df0["datetime"] es mayor que @df1["datetime"]
        -En caso de no encontrar coincidencias:
            *Si se cumple la condicion anterior, indica que no hay valores de tráfico para el "datetime" consultado
                entonces, se salta a la siguiente hora 
    """
    def file_concat_merge(self, df0, df1, columns):
        sms = "fileConcatMerge: executed"
        print(sms)
            
        res = pd.to_datetime(df0.loc[df0.index[-1], "datetime"], format="%Y-%m-%d %H:%M:%S") <= pd.to_datetime(df1["datetime"], format="%Y-%m-%d %H:%M:%S")
        if res.bool():
            """ - AUN FALTAN VALORES DE TRÁFICO 
            -- Hasta que no se registre la hora entera de tráfico no se guardan los datos
                * return false, se espera a que esten todos los valores para la hora a registrar               
            """
            sms =  "fileConcatMerge: 1T_W AUN FALTAN VALORES PARA TRÁFICO"
            return [False, df0, sms]
                
        """ ULTIMA HORA DE TRÁFICO ES MAYOR QUE LA HORA A REGISTRAR

        """
        """ 
            -- Se pasa una lista de valores y se registran cuando @datetime coincida
        """

        for i in columns[1:]:
            df0.loc[df0.datetime == df1.loc[0,"datetime"], i]= df1.loc[0, i]

        sms = "fileConcatMerge: REGISTRO CORRECTO"
        
        return[True, df0, sms]

    
    """
        - Se crean los archivos donde se guardan todos los datos, donde se guardan los datos normalizados
          y donde se guardarán las predicciones.
        - Se establece la hora a partir de la cual se harán las consultas.
    """
    def realtime_apis(self):
        
        self.utils.file_creator(self.merge_file, self.list_merge) 
        self.utils.file_creator(self.normal_data_file, self.list_normal_data)
        self.utils.file_creator(self.predict_data_file, self.list_predict_data)

        self.input_datetime = dt.strptime(str(self.ini_datetime), self.format_datetime) - timedelta(hours=self.input_width+self.out_steps+self.historic)
        self.input_datetime = str(self.input_datetime).replace(" ","T")
        
        print("=*"*50)
        print("main reailtime apis: ")
        print("start datetime: ", self.ini_datetime)
        print("input datetime: ", self.input_datetime)
        print("=*"*50)

        traffic_api_ = threading.Thread(target = self.traffic_api, args = (5*60, 1000000), name="traffic_api")
        air_api_ = threading.Thread(target= self.air_api, args = (7*60,), name="air_api")
        weather_api_ = threading.Thread(target= self.weather_api, args = (9*60,), name="weather_api" )
        traffic_api_.start()
        air_api_.start() 
        weather_api_.start()  