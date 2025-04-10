from flask import Flask, request, jsonify, g
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import pickle
import requests
import time
from werkzeug.serving import run_simple
from sklearn.preprocessing import MinMaxScaler



app = Flask(__name__)

# Carrega o scaler
try:
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
except FileNotFoundError:
    print("Error: scaler.pkl not found. Make sure the file exists in the same directory as your script.")
    scaler = None # Or handle the error appropriately, like exiting the program.
except Exception as e:
    print(f"An error occurred while loading the scaler: {e}")
    scaler = None # Handle the error.

# Carrega o modelo treinado
model = tf.keras.models.load_model('stock_prediction_model.keras')



request_counts = {}
@app.before_request
def before_request():
    g.start = time.time()
    global request_counts
    if request.path not in request_counts:
        request_counts[request.path] = 0
    request_counts[request.path] += 1

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    print(f"Request to {request.path} took {diff:.4f} seconds")
    return response

@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify(request_counts)
    
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        historical_prices = data['historical_prices']

        # Prepara os dados de entrada
        input_data = np.array(historical_prices).reshape(-1, 1)
        input_data = scaler.transform(input_data)

        # Faz a previsão
        look_back = 30 
        if len(input_data) < look_back:
            return jsonify({'error': 'Insufficient historical data'}), 400

        X_input = np.reshape(input_data[-look_back:], (1, look_back, 1))
        prediction = model.predict(X_input)

        # Inverte a escala para obter o valor real
        prediction = scaler.inverse_transform(prediction)

        return jsonify({'prediction': prediction[0][0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    run_simple('localhost', 8080, app)