from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    data = {'company': 'goog'}

    url = 'http://127.0.0.1:5000/'
    labels = requests.post(url, data=data).json()['labels']
    values = requests.post(url, data=data).json()['values']
    
    return render_template('index.html', labels=labels, values=values)
        
if __name__ == '__main__':
    app.run(debug=True, port=5001)