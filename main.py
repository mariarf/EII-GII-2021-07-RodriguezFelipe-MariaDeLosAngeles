from main_realtime_apis import MainRealtimeApis

if __name__ == "__main__":
    input_width = 12
    out_steps = 3
   
    """
        - Se establece el input_width/número de entradas y el out_steps/número de prediccciones.
        - El tercer parámetro sirve para indicar el tamaño de datos históricos que se consultan,
        sirve para cargar la web con un pequeño conjunto de datos que permitan ver como funciona
    """
    MainRealtimeApis(input_width, out_steps, 24).realtime_apis()

