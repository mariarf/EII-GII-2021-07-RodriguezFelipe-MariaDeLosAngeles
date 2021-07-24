## Models analysis

En este directorio encontrará tres documentos de tipo Jupyter Notebook escritos en python.


El primer documento `4.6.1 Anális y preparación de los datos históricos` es el documento que se 
utilizó para analizar los datos históricos recogidos entre julio de 2019 hasta junio de 2020. Es importante
tener en cuenta que, debido a que los datos pueden variar según la fecha que se desee analizar, los analisis
hechos en este documento pueden variar. En el apartado 4.6.1 de la memoria de este proyecto puede encontrar
explicaciones más detalladas acerca de las desiciones tomadas al momento de preparar los datos.


El segundo documento `4.6.2 Creación de modelos` consiste en un conjunto de clases y métodos para crear
distintos modelos de redes neuronales. El documento incluye: un modelo de base, un modelo lineal, un modelo denso,
un modelo CNN y un modelo RNN. Para generar los modelos se le indica un conjunto de datos de entrada y de salida. Estos modelos están pensados para funcionar con los datos recogidos en el primer documento para el rango de fechas de julio de 
2019 hasta junio de 2021. Al final de la ejecución de los modelos, éstos se guardan. Además, se guarda un archivo con los datos estadísticos (pérdida y error medio absoluto) de cada uno. Para más información acerca de los modelos desarrollados y las decisiones tomadas, consultar el apartado 4.6.2 en la memoria de este proyecto.


El tercer documento `4.7 Selección del modelo` está pensado para generar modelos LSTM con distintas entradas y salidas.
En el apartado 4.7 de la memoria de este proyecto se puede consultar con mayor detalle el uso de este documento.


A modo de precaución, se guardan todos los datos generados por los modelos en la carpeta new_models. En la carpeta original_models se encuentran los modelos generados durante la preparación del proyecto.
Los datos de entreno para normalizar se guardan en la carpeta `nomalize_data`. En caso de querer utilizar 
este conjunto de datos de entreno para normalizar los datos de los modelos en tiempo real, se debe reescribir el documento
dejándole como nombre `train_data.csv`.

La carpeta LSTM es la carpeta a la que se accede para generar las predicciones desde el apartado de realtime.

El archivo con los datos recolectados que se utilizó para entrenar los modelos se encuentra en la carpeta `apis\historical_apis\out_historical_apis\merge_historical\2019-2021-2Y\historical_data_2019-2021-2Y.zip`. Este archivo se comprimió debido a que pesa más de 500mb, que es el peso máximo permitido por GitHub. Por lo cual, si se quiere probar el código de los modelos, se recomienda descomprimir dicho archivo en local o volver a hacer la descarga de los datos para la fecha correspondiente.
