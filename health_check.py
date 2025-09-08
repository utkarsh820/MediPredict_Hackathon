"""
Health check script for Railway deployment.
This script helps ensure that the application is running correctly
by verifying that the model and encoder can be loaded.
"""
import os
import sys
import joblib

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def check_health():
    """
    Check if the application can load its essential components.
    Returns True if everything is working, False otherwise.
    """
    try:
        # Check if model files exist
        model_path = os.path.join(project_root, "models", "cat_disease_model.pkl")
        encoder_path = os.path.join(project_root, "models", "label_encoder.pkl")
        
        if not os.path.exists(model_path):
            print(f"Error: Model file not found at {model_path}")
            return False
            
        if not os.path.exists(encoder_path):
            print(f"Error: Encoder file not found at {encoder_path}")
            return False
        
        # Try to load the model and encoder
        print("Loading model and encoder to verify health...")
        model = joblib.load(model_path)
        encoder = joblib.load(encoder_path)
        
        if model is None or encoder is None:
            print("Error: Failed to load model or encoder")
            return False
            
        print("Health check successful: Model and encoder loaded correctly")
        return True
        
    except Exception as e:
        print(f"Health check failed: {str(e)}")
        return False

if __name__ == "__main__":
    result = check_health()
    # Exit with status code 0 if healthy, 1 if not
    sys.exit(0 if result else 1)
