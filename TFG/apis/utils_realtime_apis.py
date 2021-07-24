import pytz, os, csv
from datetime import datetime as dt
from datetime import timedelta as timedelta

class UtilsRealtimeApis():

    def get_format_datetime(self):
        return "%Y-%m-%dT%H:%M:%S"

    def get_str_ny(self):
        return 'America/New_York'

    def convert_time_str(self, time, from_time, to_time):
        from_time = pytz.timezone(from_time)
        to_time = pytz.timezone(to_time)
        format_datetime = UtilsRealtimeApis().get_format_datetime()

        res = dt.strptime(time, format_datetime)
        res = from_time.localize(res)
        res = res.astimezone(to_time)
        res = res.strftime(format_datetime)
        return res

    # Método que devuelve la diferencia entre la fecha local en NY y la fecha pasada por parámetro
    def difference_datetime(self, datetime_value):
        my_class = UtilsRealtimeApis()
        tz_ny = pytz.timezone(my_class.get_str_ny()) 
        format_datetime = my_class.get_format_datetime()
        current_datetime = dt.now(tz_ny)
        current_datetime = dt.strptime(str(current_datetime)[0:-13],"%Y-%m-%d %H:%M:%S")
        datetime_value = dt.strptime(datetime_value, format_datetime)
        return current_datetime - datetime_value

    def get_lists(self):
        list_traffic = ["datetime","datetime_traffic","weekday","speed","travel_time","link_name"]
        list_airQuality = ["datetime","AQI_PM2.5", "AQI_OZONE"]
        list_weather = ["datetime","Minimum Temperature","Maximum Temperature","Temperature","Dew Point","Relative Humidity","Wind Speed","Wind Direction","Precipitation","Precipitation Cover","Snow Depth","Visibility","Cloud Cover","Sea Level Pressure","Conditions"]
        list_merge = list_traffic + list_airQuality[1:] + list_weather[1:]
        list_normal_data = ["AQI","weekday","speed","travel_time","Minimum Temperature","Maximum Temperature","Temperature","Dew Point","Relative Humidity","Precipitation","Snow Depth","Visibility","Cloud Cover","Sea Level Pressure","Conditions","Wx","Wy","Day sin","Day cos","Year sin","Year cos"]
        list_predict_data = ["datetime","predict_aqi_t0","predict_category_t0","predict_color_t0","predict_aqi_t1","predict_category_t1","predict_color_t1","predict_aqi_t2","predict_category_t2","predict_color_t2","predict_aqi_t3","predict_category_t3","predict_color_t3","real_aqi","real_category","real_color"]
        return list_traffic, list_airQuality, list_weather, list_merge, list_normal_data, list_predict_data

    def get_realtime_apis_file_directions(self):

        current_dir = os.getcwd() + "\\apis\out_apis"

        merge_file = current_dir + "\merge.csv"
        traffic_file = current_dir + "\data_apis\\traffic.csv"
        air_quality_file = current_dir + "\data_apis\\airQuality.csv"
        weather_file = current_dir + "\data_apis\weather.csv"
        normal_data_file = os.getcwd() + "\in\\normalize_data\\normal_data.csv"
        predict_data_file = os.getcwd() + "\out\predictions\predictions.csv"


        return traffic_file, air_quality_file, weather_file, merge_file, normal_data_file, predict_data_file

    """ fileCreator:
        *** recibe una direccion/path @file_name y una lista @list con nombres de columnas
        - crea el archivo y le asigna @list como cabecera
    """
    def file_creator(self, file_name, list): 
        print("file_creator: ", file_name)

        file = open(file_name, 'w')
        with file:
            # cabecera
            writer = csv.DictWriter(file, fieldnames = list)
            # se escribe la cabecera en el archivo
            writer.writeheader()
