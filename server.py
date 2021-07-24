from flask import Flask, make_response, redirect, render_template

from werkzeug.utils import redirect
from flask_bootstrap import Bootstrap

from utils.server_utils import ServerUtils

app = Flask(__name__)
bootstrap = Bootstrap(app)
server_utils = ServerUtils()

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html')

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html')

@app.route('/', methods=['GET'])
def index():
    response = make_response(redirect('/predict'))
    return response

@app.route('/predict', methods=['GET'])
def predict():
    date, actual_aqi = server_utils.get_basic_data()

    predictions = server_utils.get_predict_t(25,0)
    if predictions.empty:
        return render_template('error.html')
    
    context = {
        'date': date,
        'predictions':predictions,
        'actual_aqi': actual_aqi
    }

    return render_template('index.html', **context )
   
@app.route('/statistics', methods=['GET'])
def statistic_data():
    tail = 25
    date, actual_aqi = server_utils.get_basic_data()

    predictions = server_utils.get_predict_t(tail,0)
    if predictions.empty:
        return render_template('error.html')
        
    context = {
        'date': date,
        'pred_t0': predictions,
        'pred_t1':  server_utils.get_predict_t(tail, 1),
        'pred_t2':  server_utils.get_predict_t(tail, 2),
        'pred_t3':  server_utils.get_predict_t(tail, 3),
        'actual_aqi': actual_aqi
    }

    return render_template('statistics.html', **context )

@app.route('/table', methods=['GET'])
def table_view():
    date, actual_aqi = server_utils.get_basic_data()

    predictions = server_utils.get_predict_t(25,0).sort_values('datetime',ascending=False)
    if predictions.empty:
        return render_template('error.html')

    context = {
        'date': date,
        'predictions': predictions,
        'actual_aqi': actual_aqi
    }

    return render_template('table_view.html', **context )