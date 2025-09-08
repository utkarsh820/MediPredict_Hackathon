import os
import joblib
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, classification_report
from src.utils.helpers import logging, CustomException

def init_catboost_model(params=None):
    default_params = {
        'iterations': 200,
        'learning_rate': 0.05,
        'depth': 6,
        'random_state': 42,
        'verbose': 0
    }
    
    if params:
        default_params.update(params)
    
    return CatBoostClassifier(**default_params)

def train_catboost_model(X_train, y_train, params=None):
    try:
        model = init_catboost_model(params)
        
        logging.info("Training CatBoost model...")
        model.fit(X_train, y_train)
        logging.info("CatBoost model training completed")
        
        return model
    except Exception as e:
        raise CustomException(f"Error training CatBoost model: {e}")

def evaluate_model(model, X_test, y_test):
    try:
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        logging.info(f"Model evaluation - Accuracy: {accuracy:.4f}")
        
        return {
            'accuracy': accuracy,
            'classification_report': report
        }
    except Exception as e:
        raise CustomException(f"Error evaluating model: {e}")

def save_model(model, le, model_dir='models'):
    try:
        os.makedirs(model_dir, exist_ok=True)
        
        model_path = os.path.join(model_dir, 'cat_disease_model.pkl')
        le_path = os.path.join(model_dir, 'label_encoder.pkl')
        
        joblib.dump(model, model_path)
        joblib.dump(le, le_path)
        
        logging.info(f"Model saved to {model_path}")
        logging.info(f"Label encoder saved to {le_path}")
        
        return True
    except Exception as e:
        raise CustomException(f"Error saving model: {e}")

def save_feature_names(feature_names, model_dir='models'):
    try:
        os.makedirs(model_dir, exist_ok=True)
        
        feature_path = os.path.join(model_dir, 'feature_names.pkl')
        joblib.dump(feature_names, feature_path)
        
        logging.info(f"Feature names saved to {feature_path}")
        
        return True
    except Exception as e:
        raise CustomException(f"Error saving feature names: {e}")

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
