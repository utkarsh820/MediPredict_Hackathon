import os
import pandas as pd
import joblib
from src.utils.helpers import logging, CustomException

def load_model(model_dir='models'):
    try:
        model_path = os.path.join(model_dir, 'cat_disease_model.pkl')
        le_path = os.path.join(model_dir, 'label_encoder.pkl')
        
        model = joblib.load(model_path)
        le = joblib.load(le_path)
        
        logging.info("Model loaded successfully")
        
        return model, le
    except Exception as e:
        raise CustomException(f"Error loading model: {e}")

def get_feature_names(model_dir='models'):
    try:
        feature_path = os.path.join(model_dir, 'feature_names.pkl')
        feature_names = joblib.load(feature_path)
        
        return feature_names
    except Exception as e:
        raise CustomException(f"Error loading feature names: {e}")

def preprocess_input(symptoms_dict):
    try:
        # Get all possible features
        all_symptoms = get_feature_names()
        
        # Create a dataframe with all features set to 0
        input_data = pd.DataFrame(0, index=[0], columns=all_symptoms)
        
        # Set the symptoms that are present
        for symptom, value in symptoms_dict.items():
            if symptom in input_data.columns:
                input_data[symptom] = value
            else:
                logging.warning(f"Symptom '{symptom}' not found in the model features")
        
        return input_data
    except Exception as e:
        raise CustomException(f"Error preprocessing input: {e}")

def predict_disease(symptoms_dict):
    try:
        # Load model and label encoder
        model, le = load_model()
        
        # Preprocess input
        input_data = preprocess_input(symptoms_dict)
        
        # Make prediction
        prediction_encoded = model.predict(input_data)[0]
        prediction = le.inverse_transform([prediction_encoded])[0]
        
        # Get probability scores
        probabilities = model.predict_proba(input_data)[0]
        max_prob = probabilities[prediction_encoded]
        
        logging.info(f"Prediction: {prediction} with confidence {max_prob:.4f}")
        
        return {
            "disease": prediction,
            "confidence": float(max_prob)
        }
    except Exception as e:
        raise CustomException(f"Error making prediction: {e}")

def get_top_symptoms_for_disease(disease, data_path='data/processed/cleaned_data.csv', top_n=5):
    try:
        # Load the data
        data = pd.read_csv(data_path)
        
        # Filter data for the specified disease
        disease_data = data[data['prognosis'] == disease]
        
        if disease_data.empty:
            logging.warning(f"No data found for disease: {disease}")
            return []
        
        # Get symptom columns (all columns except 'prognosis')
        symptom_cols = [col for col in data.columns if col != 'prognosis']
        
        # Calculate symptom frequencies for this disease
        symptom_counts = disease_data[symptom_cols].sum().sort_values(ascending=False)
        
        # Get top symptoms
        top_symptoms = symptom_counts.head(top_n)
        
        result = [{"symptom": symptom, "count": int(count)} 
                 for symptom, count in top_symptoms.items()]
        
        return result
    except Exception as e:
        raise CustomException(f"Error getting top symptoms for disease: {e}")
