import pytest
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'best_model.pkl')

PERFORMANCE_THRESHOLDS = {
    'accuracy': 0.85,
    'precision_macro': 0.80,
    'recall_macro': 0.80,
    'f1_macro': 0.80
}

@pytest.fixture
def model_data():
    if not os.path.exists(MODEL_PATH):
        pytest.skip("Modelo não encontrado. Execute o notebook primeiro.")
    
    model_data = joblib.load(MODEL_PATH)
    return model_data

@pytest.fixture
def test_data():
    from ucimlrepo import fetch_ucirepo
    
    car_evaluation = fetch_ucirepo(id=19)
    X = car_evaluation.data.features
    y = car_evaluation.data.targets
    
    from sklearn.model_selection import train_test_split
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    return X_test, y_test

def test_model_exists():
    assert os.path.exists(MODEL_PATH), "Arquivo do modelo não encontrado"

def test_model_loads(model_data):
    assert 'model' in model_data, "Modelo não encontrado no arquivo"
    assert 'label_encoders' in model_data, "Label encoders não encontrados"
    assert model_data['model'] is not None, "Modelo está vazio"

def test_model_has_required_methods(model_data):
    model = model_data['model']
    assert hasattr(model, 'predict'), "Modelo não possui método predict"
    assert hasattr(model, 'classes_'), "Modelo não possui classes_"

def test_model_accuracy(model_data, test_data):
    model = model_data['model']
    label_encoders = model_data['label_encoders']
    X_test, y_test = test_data
    
    X_test_encoded = X_test.copy()
    for col in X_test_encoded.columns:
        if col in label_encoders:
            X_test_encoded[col] = label_encoders[col].transform(X_test_encoded[col])
    
    y_pred = model.predict(X_test_encoded)
    
    accuracy = accuracy_score(y_test, y_pred)
    
    assert accuracy >= PERFORMANCE_THRESHOLDS['accuracy'], \
        f"Acurácia {accuracy:.4f} abaixo do threshold {PERFORMANCE_THRESHOLDS['accuracy']}"

def test_model_precision(model_data, test_data):
    model = model_data['model']
    label_encoders = model_data['label_encoders']
    X_test, y_test = test_data
    
    X_test_encoded = X_test.copy()
    for col in X_test_encoded.columns:
        if col in label_encoders:
            X_test_encoded[col] = label_encoders[col].transform(X_test_encoded[col])
    
    y_pred = model.predict(X_test_encoded)
    
    precision = precision_score(y_test, y_pred, average='macro')
    
    assert precision >= PERFORMANCE_THRESHOLDS['precision_macro'], \
        f"Precisão macro {precision:.4f} abaixo do threshold {PERFORMANCE_THRESHOLDS['precision_macro']}"

def test_model_recall(model_data, test_data):
    model = model_data['model']
    label_encoders = model_data['label_encoders']
    X_test, y_test = test_data
    
    X_test_encoded = X_test.copy()
    for col in X_test_encoded.columns:
        if col in label_encoders:
            X_test_encoded[col] = label_encoders[col].transform(X_test_encoded[col])
    
    y_pred = model.predict(X_test_encoded)
    
    recall = recall_score(y_test, y_pred, average='macro')
    
    assert recall >= PERFORMANCE_THRESHOLDS['recall_macro'], \
        f"Recall macro {recall:.4f} abaixo do threshold {PERFORMANCE_THRESHOLDS['recall_macro']}"

def test_model_f1_score(model_data, test_data):
    model = model_data['model']
    label_encoders = model_data['label_encoders']
    X_test, y_test = test_data
    
    X_test_encoded = X_test.copy()
    for col in X_test_encoded.columns:
        if col in label_encoders:
            X_test_encoded[col] = label_encoders[col].transform(X_test_encoded[col])
    
    y_pred = model.predict(X_test_encoded)
    
    f1 = f1_score(y_test, y_pred, average='macro')
    
    assert f1 >= PERFORMANCE_THRESHOLDS['f1_macro'], \
        f"F1-Score macro {f1:.4f} abaixo do threshold {PERFORMANCE_THRESHOLDS['f1_macro']}"

def test_model_predictions_shape(model_data, test_data):
    model = model_data['model']
    label_encoders = model_data['label_encoders']
    X_test, y_test = test_data
    
    X_test_encoded = X_test.copy()
    for col in X_test_encoded.columns:
        if col in label_encoders:
            X_test_encoded[col] = label_encoders[col].transform(X_test_encoded[col])
    
    y_pred = model.predict(X_test_encoded)
    
    assert len(y_pred) == len(y_test), "Número de predições não corresponde ao número de amostras"
    assert y_pred.shape == y_test.values.ravel().shape, "Shape das predições incompatível"

def test_model_valid_classes(model_data, test_data):
    model = model_data['model']
    label_encoders = model_data['label_encoders']
    X_test, y_test = test_data
    
    X_test_encoded = X_test.copy()
    for col in X_test_encoded.columns:
        if col in label_encoders:
            X_test_encoded[col] = label_encoders[col].transform(X_test_encoded[col])
    
    y_pred = model.predict(X_test_encoded)
    
    valid_classes = set(['unacc', 'acc', 'good', 'vgood'])
    pred_classes = set(y_pred)
    
    assert pred_classes.issubset(valid_classes), \
        f"Modelo previu classes inválidas: {pred_classes - valid_classes}"

if __name__ == "__main__":
    pytest.main([__file__, '-v'])
