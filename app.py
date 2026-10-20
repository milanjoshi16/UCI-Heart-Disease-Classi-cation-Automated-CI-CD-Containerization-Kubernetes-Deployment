from flask import Flask, render_template, request
import joblib
import numpy as np
import os
import warnings
from sklearn.exceptions import InconsistentVersionWarning

# Suppress unpickling version warnings and feature name warnings for clean execution
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'models', 'heart_model.pkl')
scaler_path = os.path.join(BASE_DIR, 'models', 'scaler.pkl')

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

FEATURE_NAMES = [
    'Age [Age in years]', 
    'Sex [Gender Identification]', 
    'Chest Pain Type [cp]', 
    'Resting Blood Pressure [trestbps]',
    'Serum Cholesterol [chol]', 
    'Fasting Blood Sugar [fbs]', 
    'Resting ECG [restecg]',
    'Max Heart Rate [thalach]', 
    'Exercise Induced Angina [exang]', 
    'ST Depression [oldpeak]',
    'ST Slope [slope]', 
    'Major Vessels Count [ca]', 
    'Thalassemia [thal]'
]

@app.route('/')
def home():
    return render_template('index.html', prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        raw_features = [
            float(request.form['age']),
            float(request.form['sex']),
            float(request.form['cp']),
            float(request.form['trestbps']),
            float(request.form['chol']),
            float(request.form['fbs']),
            float(request.form['restecg']),
            float(request.form['thalach']),
            float(request.form['exang']),
            float(request.form['oldpeak']),
            float(request.form['slope']),
            float(request.form['ca']),
            float(request.form['thal'])
        ]
        
        input_arr = np.array(raw_features).reshape(1, -1)
        scaled_arr = scaler.transform(input_arr)
        
        prediction = int(model.predict(scaled_arr)[0])
        probabilities = model.predict_proba(scaled_arr)[0].tolist()
        confidence = round(float(np.max(probabilities)) * 100, 2)
        
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        else:
            importances = np.abs(model.coef_[0])
            
        feature_impacts = sorted(zip(FEATURE_NAMES, importances, raw_features), key=lambda x: x[1], reverse=True)
        top_features = feature_impacts[:5]
        
        chart_labels = [f[0] for f in top_features]
        chart_values = [round(float(f[1]) * 100, 2) for f in top_features]
        
        # Advanced chart data (Seaborn-style statistical scatter & trend data)
        scatter_x = [f[2] for f in top_features]  # Patient's actual input values for top features
        scatter_y = chart_values                  # Model feature importance weights
        
        trend_labels = ['Age', 'BP', 'Chol', 'HR', 'Oldpeak']
        trend_patient_vals = [raw_features[0], raw_features[3], raw_features[4], raw_features[7], raw_features[9]]
        trend_normal_means = [54.0, 120.0, 215.0, 150.0, 0.8] # Population reference baselines

        return render_template(
            'index.html',
            prediction=prediction,
            confidence=confidence,
            probabilities=probabilities,
            chart_labels=chart_labels,
            chart_values=chart_values,
            scatter_x=scatter_x,
            scatter_y=scatter_y,
            trend_labels=trend_labels,
            trend_patient_vals=trend_patient_vals,
            trend_normal_means=trend_normal_means,
            form_data=request.form
        )
    except Exception as e:
        return render_template('index.html', prediction=None, error=str(e))

if __name__ == '__main__':
    app.run(debug=True, port=5000)