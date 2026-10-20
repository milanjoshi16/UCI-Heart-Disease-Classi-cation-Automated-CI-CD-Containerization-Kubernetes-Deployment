import os
import pytest
from src.predict import app

def test_data_existence():
    path = '../data/processed/cleaned_heart.csv'
    if not os.path.exists(path):
        path = 'data/processed/cleaned_heart.csv'
    assert os.path.exists(path), "Cleaned dataset must exist."

def test_model_artifact_existence():
    path = '../models/heart_model.pkl'
    if not os.path.exists(path):
        path = 'models/heart_model.pkl'
    assert os.path.exists(path), "Trained model artifact must exist."

def test_flask_health_endpoint():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'