import pandas as pd
import os
from datetime import timedelta as timedelta
from datetime import datetime as dt
from tensorflow import keras

from utils.window_generator import WindowGenerator
from utils.data_processing import DataProcessing
from utils.predictions_processing import PredictionsProcessing

class Model:

    def __init__(self, input_width, out_steps):
        print('·-'*60)
        print("Model: _init_")
        print('·-'*60)
        self.model_path = f'./models/LSTM/multi_lstm_model_input_{input_width}_out_{out_steps}.h5'
        self.normal_path = os.getcwd() + f"/in/normalize_data/normal_data.csv"
        
        self.prediction_processing = PredictionsProcessing()
        self.data_processing = DataProcessing()

        self.input_width = input_width
        self.out_steps = out_steps

    def predict_results(self, hour_datetime):
        data_df = pd.read_csv(self.normal_path, low_memory=False)
        model = keras.models.load_model(self.model_path)
        
        print("-/"*60)
        print("predict results: ", hour_datetime)
        print("-/"*60)

        # Si se cuenta con los datos suficientes se reentrena el modelo
        window_len = self.input_width + self.out_steps
        if len(data_df) >= window_len:
            multi_window_train = WindowGenerator(input_width=self.input_width,
                                                label_width=self.out_steps,
                                                shift=self.out_steps,
                                                data_df=data_df,
                                                label_columns=['AQI'])
            model.fit(multi_window_train.data, epochs=20)

        # Se generan las predicciones correspondientes
        col = data_df.columns.get_loc('AQI')
    
        window = WindowGenerator(input_width=self.input_width,
                                label_width=0,
                                shift=0,
                                data_df=data_df,
                                label_columns=['AQI'])

        predictions = model.predict(window.data)
        
        # Se desnormalizan los resultados y se guardan en ./out/predictions
        num = 0
        while num < self.out_steps:
            normal_value = predictions[0, num, col]
            value = self.data_processing.denormalize_data(normal_value, col)

            hour_datetime = dt.strptime(str(hour_datetime), "%Y-%m-%d %H:%M:%S") + timedelta(hours=1)
            self.prediction_processing.add_value(hour_datetime, True, value, 0)
            self.prediction_processing.add_value(hour_datetime, True, value, num+1)

            num += 1

        model.save(self.model_path)