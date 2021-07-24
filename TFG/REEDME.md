# TFG 

Este repositorio está dividido en tres partes principales que funcionan de forma independiente.

    1. Obtención de datos históricos
    
    2. Análisis de los datos y creación de modelos
    
    3. Desarrollo de página web

Para el primer apartado, navegar hasta la carpeta `apis/historical_apis`. Dentro de esa carpeta
encontrá un documento REEDME.md que le indicará el funcionamiento de este apartado.

Para el segundo apartado, navegar hasta la carpeta `models/models_analysis`. Dentro de esa carpeta
encontrá un documento REEDME.md que le indicará el funcionamiento de este apartado.

El tercer apartado se explicará en este documento. A continuación, se explicarán los archivos tipo .py que se encuentran en la raíz del directorio:
    
    
  1. main_realtime_apis: es la clase encargada de consultar en tiempo real los datos a las APIs. 
    Para esto, utiliza las clases definidas en la raíz de la carpeta `apis`. Una vez registrados los 
    datos de una hora entera,consulta a las clases definidas en la carpeta `utils`, en donde procesa los datos, l
    os guarda y llama a la clase encargada de reentrenar el modelo y generar las predicciones.
        a- model.py: en este documento se definen los metodos necesarios para reentrenar los modelos y 
        generar las predicciones y guardar las nuevas predicciones en el documento encargado de
        proporcionar los datos utilizados por la web.
    
  2. main: es el método principal que se encarga de ejecutar la clase `main_real_time`.
    Aquí se define el número de entradas y de salidas del modelo que se desea utilizar y se le pasa a la clase `main_real_time`.
    
  3. server.py: este documento se utiliza para crear y cargar la web donde se observarán las predicciones generadas por el modelo en tiempo real. 
    Utiliza dentro de la carpeta `utils/server_utils.py` la clase ServerUtils para cargar los datos que se utilizarán en la web. 
    La carpeta `templates` y `static` contienen los archivos necesarios para generar el sitio web.

Para probar este tercer apartado es tan simple como ejecutar el método `main`. La primera vez se debe esperar durante cierto tiempo hasta que se carguen los datos necesarios para cargar la web y empezar a generar predicciones. En la memoria de este proyecto se encuentra detallado el funcionamiento de estos métodos.

Posteriormente, para ejecutar la web se debe introducir en la terminal:
    `set FLASK_APP=server.py`
    `set FLAS_DEBUG=1`
    `flask run`

Luego ingresar en el navegador en el siguiente enlace: http://127.0.0.1:5000/predict

Versión de Python 3.8.7
Librerías y paquetes necesarios:

    - pip install pandas
    - pip install matplotlib
    - pip install sodapy
    - pip install IPython
    - pip install tensorflow
    - pip install flask
    - pip install flask-bootstrap

**Importante**
Si durante la recolección de los datos salta algún error, se debe a que se ha excedido el límite de solicitudes mensuales a la API del clima. Esto normalmente no sucede, pero puede pasar que si hay muchas personas usando el proyecto con la misma Key, se llegue al máximo de solicitudes antes de lo previsto.

Para solicitar una nueva Key debe hacerlo a través del enlace: https://rapidapi.com/visual-crossing-corporation-visual-crossing-corporation-default/api/visual-crossing-weather/

Posteriormente, se tendrá que reemplazar las keys en el archivo `apis\api_weather.py` en las líneas 14 y 17.
