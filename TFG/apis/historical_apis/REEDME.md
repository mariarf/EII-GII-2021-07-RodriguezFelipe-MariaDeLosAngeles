## Historical API

Dentro de este directorio (`apis/historical_apis`) encontrará un conjunto de clases y métodos que funcionan para generar solicitudes a las distintas APIs de este proyecto y recolectar la información en un único documento.

Si se desea descargar un conjunto de datos históricos se puede hacer desde main_historical_apis.py llamando al método `apis_request("yyyy-mm", number_of_month, "file_name")`

A este método se le proporciona un año y un mes, un número de meses y el nombre del archivo en el que se desea guardar la dirección donde se guarda es `apis\historical_apis\out_historical_apis\merge_historical\file_name` y se genera un documento con los datos históricos a partir de la fecha que se le propociona hasta el número de meses indicado

**IMPORTANTE** Si durante la recolección de los datos salta algún error, se debe a que se ha excedido el límite de solicitudes mensuales a la API del clima. Esto normalmente no sucede, pero puede pasar que si hay muchas personas usando el proyecto con la misma Key, se llegue al máximo de solicitudes antes de lo previsto.

Para solicitar una nueva Key debe hacerlo a través del enlace: https://rapidapi.com/visual-crossing-corporation-visual-crossing-corporation-default/api/visual-crossing-weather/

Posteriormente se tendrá que reemplazar las keys en el archivo `apis\historical_apis\historical_api_weather.py` en la línea 16.

El archivo con los datos recolectados que se utilizó para entrenar los modelos se encuentra en la carpeta `apis\historical_apis\out_historical_apis\merge_historical\2019-2021-2Y\historical_data_2019-2021-2Y.zip`. Este archivo se comprimió debido a que pesa más de 500mb, que es el peso máximo permitido por GitHub. Por lo cual, si se quiere probar el código de los modelos, se recomienda descomprimir dicho archivo en local o volver a hacer la descarga de los datos para la fecha correspondiente.