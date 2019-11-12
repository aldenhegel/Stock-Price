from flask import Flask, render_template, request, send_from_directory, jsonify
import pandas as pd 
import numpy as np 
import requests
import json
import datetime
import calendar
import joblib
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        company = request.form
        company = company['company']

        data = pd.read_csv(f'{company.upper()}.csv')
        data.set_index('timestamp', inplace=True)
        data.sort_index(inplace=True)

        date_list = [date.replace('-', ' ') for date in list(data.head(7).index)]

        tomorrow = str(datetime.date.today() + datetime.timedelta(days=1))
        tomorrow = tomorrow.replace('-', ' ')

        date_list.append(tomorrow)

        close_list = list(data.tail(7)['close'].values)

        scaler = MinMaxScaler(feature_range=(0,1))
        x_scaled = scaler.fit_transform(data.tail(60)['close'].values.reshape(-1, 1))

        with graph.as_default():
            y_scaled = model.predict(x_scaled.reshape(1, 60, 1))

        y = scaler.inverse_transform(y_scaled)[0][0].astype('float64')

        close_list.append(y)

        labels = []
        for i in date_list:
            labels.append(findDay(i))

        return jsonify({
            'labels': labels,
            'values': close_list
        })

@app.errorhandler(404)
def notFound(error):
    return render_template('404.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

if __name__ == '__main__':
    def findDay(date): 
        born = datetime.datetime.strptime(date, '%Y %m %d').weekday() 
        return (calendar.day_name[born]) 

    model = joblib.load('lstm_presentation')

    graph = tf.get_default_graph()

    app.run(debug = True)