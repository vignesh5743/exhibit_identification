from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

svm_model = joblib.load('svm_model.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():

    data = request.get_json()
    
    required_keys = {'Type', 'Current', 'Vibration'}
    if not required_keys.issubset(data.keys()):
        return jsonify({'error': 'Missing one or more required fields: Type, Current, Vibration'}), 400
    
    type_value = data['Type']
    current_value = data['Current']
    vibration_value = data['Vibration']
    
    if type_value == 1:
        # Type 1: Check if Current value is <= 0
        if current_value <= 0:
            return jsonify({'prediction': 'Alert'})
        else:
            return jsonify({'prediction': 'Normal'})
    
    elif type_value == 2:
        # Type 2: Check if Current has a value but Vibration is not set
        if current_value > 0 and vibration_value == 0:
            return jsonify({'prediction': 'Alert'})
        else:
            return jsonify({'prediction': 'Normal'})
    
    elif type_value == 3:
        # Type 3: Check Current and Vibration
        if vibration_value == 1:
            return jsonify({'prediction': 'Normal'})
        elif current_value < 0:
            return jsonify({'prediction': 'Alert'})
        else:
            return jsonify({'prediction': 'Normal'})
    
    else:
        return jsonify({'error': 'Invalid Type value'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
