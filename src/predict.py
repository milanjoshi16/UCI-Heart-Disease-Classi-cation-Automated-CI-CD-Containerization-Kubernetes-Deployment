from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
import logging

app = Flask(__name__)

# Configure request logging (Task 8)
logging.basicConfig(level=logging.INFO)

# Load model and scaler
model_path = os.path.join(os.path.dirname(__file__), '../models/heart_model.pkl')
scaler_path = os.path.join(os.path.dirname(__file__), '../models/scaler.pkl')

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "message": "Heart Disease MLOps API is running"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        features = data.get('features')
        
        if not features:
            return jsonify({"error": "No features provided"}), 400
        
        features_arr = np.array(features).reshape(1, -1)
        
        # Make prediction and compute confidence score
        prediction = int(model.predict(features_arr)[0])
        confidence = float(np.max(model.predict_proba(features_arr)))
        
        app.logger.info(f"API Request processed successfully. Prediction: {prediction}, Confidence: {confidence:.2f}")
        
        return jsonify({
            "prediction": prediction,
            "confidence": confidence,
            "status": "success"
        })
    except Exception as e:
        app.logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)