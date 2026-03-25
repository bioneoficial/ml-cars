from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'best_model.pkl')
model = None
label_encoders = None

def load_model():
    global model, label_encoders
    try:
        model_data = joblib.load(MODEL_PATH)
        model = model_data['model']
        label_encoders = model_data['label_encoders']
        print("Modelo carregado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao carregar modelo: {e}")
        return False

@app.route('/')
def home():
    return jsonify({
        "message": "API de Classificação de Avaliação de Carros",
        "status": "online",
        "model_loaded": model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Modelo não carregado"}), 500
    
    try:
        data = request.json
        
        required_fields = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo '{field}' é obrigatório"}), 400
        
        input_data = pd.DataFrame([{
            'buying': data['buying'],
            'maint': data['maint'],
            'doors': data['doors'],
            'persons': data['persons'],
            'lug_boot': data['lug_boot'],
            'safety': data['safety']
        }])
        
        for col in input_data.columns:
            if col in label_encoders:
                try:
                    input_data[col] = label_encoders[col].transform(input_data[col])
                except ValueError as e:
                    return jsonify({
                        "error": f"Valor inválido para '{col}': {data[col]}"
                    }), 400
        
        prediction = model.predict(input_data)[0]
        probabilities = None
        
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(input_data)[0]
            probabilities = {
                model.classes_[i]: float(proba[i]) 
                for i in range(len(model.classes_))
            }
        
        class_mapping = {
            'unacc': 'Unacceptable',
            'acc': 'Acceptable',
            'good': 'Good',
            'vgood': 'Very Good'
        }
        
        return jsonify({
            "prediction": prediction,
            "prediction_label": class_mapping.get(prediction, prediction),
            "probabilities": probabilities,
            "input": data
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    if model is None:
        return jsonify({"error": "Modelo não carregado"}), 500
    
    info = {
        "model_type": type(model).__name__,
        "features": ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety'],
        "classes": list(model.classes_) if hasattr(model, 'classes_') else None,
        "expected_values": {
            "buying": ["vhigh", "high", "med", "low"],
            "maint": ["vhigh", "high", "med", "low"],
            "doors": ["2", "3", "4", "5more"],
            "persons": ["2", "4", "more"],
            "lug_boot": ["small", "med", "big"],
            "safety": ["low", "med", "high"]
        }
    }
    
    return jsonify(info)

if __name__ == '__main__':
    if load_model():
        app.run(debug=True, port=5000)
    else:
        print("AVISO: Iniciando servidor sem modelo. Execute o notebook primeiro para gerar o modelo.")
        app.run(debug=True, port=5000)
