import os
import sys
import subprocess

# Try to import required packages, install if not available
try:
    import pandas as pd
except ImportError:
    print("Installing pandas...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd

try:
    import joblib
except ImportError:
    print("Installing joblib...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "joblib"])
    import joblib

try:
    from flask import Flask, request, jsonify, render_template, url_for, redirect
except ImportError:
    print("Installing Flask...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, request, jsonify, render_template, url_for, redirect

# Add the project root to Python path so we can import from src
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Initialize Flask application with template and static folders
app = Flask(
    __name__, 
    template_folder=os.path.join(project_root, "templates"),
    static_folder=os.path.join(project_root, "static")
)

# Define paths to model files
MODEL_PATH = os.path.join(project_root, "models", "cat_disease_model.pkl")
ENCODER_PATH = os.path.join(project_root, "models", "label_encoder.pkl")

# Global variables for model and encoder (load once)
_model = None
_encoder = None

# Load model and encoder
def load_model():
    global _model, _encoder
    
    # If already loaded, return cached model
    if _model is not None and _encoder is not None:
        return _model, _encoder
        
    try:
        print(f"Loading model from {MODEL_PATH}...")
        _model = joblib.load(MODEL_PATH)
        print(f"Loading encoder from {ENCODER_PATH}...")
        _encoder = joblib.load(ENCODER_PATH)
        print("Model and encoder loaded successfully")
        return _model, _encoder
    except Exception as e:
        print(f"Error loading model or encoder: {str(e)}")
        return None, None

# Hard-coded feature names in the correct order (from model inspection)
MODEL_FEATURES = [
    'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 
    'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 
    'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 
    'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 
    'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 
    'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 
    'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 
    'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 
    'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 
    'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 
    'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 
    'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 
    'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 
    'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 
    'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 
    'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 
    'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 
    'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 
    'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 
    'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 
    'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 
    'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 
    'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 
    'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 
    'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 
    'altered_sensorium', 'red_spots_over_body', 'belly_pain', 
    'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 
    'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 
    'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 
    'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 
    'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 
    'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf', 
    'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 
    'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 
    'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze'
]

# Function to get feature names in correct order
def get_feature_names():
    # Return the hardcoded feature names that match the model
    return MODEL_FEATURES

# Dictionary to map from dataset names to model feature names 
# to handle mismatches between dataset column names and model feature names
FEATURE_NAME_MAPPING = {
    'spotting_urination': 'spotting_ urination',
    'foul_smell_of_urine': 'foul_smell_of urine',
    'dischromic_patches': 'dischromic _patches',
    'blood_in_sputum': 'fluid_overload.1',
    'prominent_veins_on_calf': 'blood_in_sputum',
    'palpitations': 'prominent_veins_on_calf',
    'painful_walking': 'palpitations',
    'pus_filled_pimples': 'painful_walking',
    'blackheads': 'pus_filled_pimples',
    'scurring': 'blackheads',
    'skin_peeling': 'scurring',
    'silver_like_dusting': 'skin_peeling',
    'small_dents_in_nails': 'silver_like_dusting',
    'inflammatory_nails': 'small_dents_in_nails',
    'blister': 'inflammatory_nails',
    'red_sore_around_nose': 'blister',
    'yellow_crust_ooze': 'red_sore_around_nose'
}

# Function to preprocess input data
def preprocess_input(symptoms_dict):
    try:
        # Use the hardcoded feature names in the correct order
        feature_names = get_feature_names()
        
        # Create a dataframe with all symptoms set to 0, in the correct order
        input_data = pd.DataFrame(0, index=[0], columns=feature_names)
        
        # Set the symptoms that are present to 1
        for symptom, value in symptoms_dict.items():
            # Check if we need to map this symptom name
            model_symptom = FEATURE_NAME_MAPPING.get(symptom, symptom)
            
            if model_symptom in input_data.columns:
                input_data[model_symptom] = value
                if symptom != model_symptom:
                    print(f"Mapped '{symptom}' to '{model_symptom}'")
            else:
                print(f"Warning: Symptom '{symptom}' not found in model features")
        
        return input_data
    except Exception as e:
        print(f"Error preprocessing input: {str(e)}")
        return None

# Function to predict disease
def predict_disease(symptoms_dict):
    # Load model and encoder
    model, encoder = load_model()
    if model is None or encoder is None:
        raise Exception("Failed to load model or encoder")
    
    # Preprocess input
    input_data = preprocess_input(symptoms_dict)
    if input_data is None:
        raise Exception("Failed to preprocess input")
    
    # Make prediction
    prediction_encoded = model.predict(input_data)[0]
    prediction = encoder.inverse_transform([prediction_encoded])[0]
    
    # Get probability scores
    probabilities = model.predict_proba(input_data)[0]
    
    # Convert prediction_encoded to integer index
    if isinstance(prediction_encoded, (int, float)):
        # If it's already a numeric index
        max_prob = probabilities[int(prediction_encoded)]
    else:
        # If it's a numpy array or other type, find the max probability
        max_prob = probabilities.max()
    
    print(f"Prediction: {prediction} with confidence {float(max_prob):.4f}")
    
    return {
        "disease": str(prediction),
        "confidence": float(max_prob)
    }

# Function to get top symptoms for a disease
def get_top_symptoms_for_disease(disease_name, top_n=5):
    try:
        # Load the data
        data_path = os.path.join(project_root, "data", "processed", "cleaned_data.csv")
        data = pd.read_csv(data_path)
        
        # Filter data for the specified disease
        disease_data = data[data['prognosis'] == disease_name]
        
        if disease_data.empty:
            print(f"No data found for disease: {disease_name}")
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
        print(f"Error getting top symptoms: {str(e)}")
        return []

@app.route('/')
def index():
    # Render the main HTML template for web interface
    return render_template('index.html')

@app.route('/api')
def api_index():
    # API information endpoint
    return jsonify({
        "message": "MediPredict API is running correctly.",
        "available_endpoints": ["/health", "/predict", "/symptoms", "/disease/<disease_name>"]
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"}), 200

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    try:
        # Check for model file
        if not os.path.exists(MODEL_PATH):
            error_msg = f"CatBoost model file not found at {MODEL_PATH}"
            print(f"ERROR: {error_msg}")
            return jsonify({"error": error_msg}), 500
        
        # Handle both GET and POST requests
        if request.method == 'GET':
            # Process GET parameters (from web form)
            # Identify checkbox inputs which have symptoms
            symptoms = {}
            for key in request.args:
                if key.startswith('symptom-'):
                    symptom_name = key.replace('symptom-', '')
                    symptoms[symptom_name] = 1
            
            # If no symptoms provided via GET, just show the form again
            if not symptoms:
                # If this is a form submission with no symptoms, redirect to form
                if request.args:
                    return redirect(url_for('index'))
                
                # Otherwise, we're accessing directly via GET API, return error
                return jsonify({"error": "No symptoms provided"}), 400
                
        else:  # POST request (from API)
            # Get symptoms from request body JSON
            data = request.json
            if not data:
                return jsonify({"error": "Invalid JSON payload"}), 400
                
            symptoms = data.get('symptoms', {})
            
            if not symptoms:
                return jsonify({"error": "No symptoms provided"}), 400
        
        # Make prediction using CatBoost model
        result = predict_disease(symptoms)
        
        # Get related symptoms
        related_symptoms = get_top_symptoms_for_disease(result['disease'])
        
        # Return prediction and related info
        response = {
            "prediction": result['disease'],
            "confidence": result['confidence'],
            "related_symptoms": related_symptoms,
            "model_used": "cat_disease_model"  # Explicitly indicate which model was used
        }
        
        return jsonify(response), 200
    
    except FileNotFoundError as e:
        error_message = f"Required model file not found: {str(e)}"
        print(f"ERROR: {error_message}")
        return jsonify({"error": error_message}), 500
    except ValueError as e:
        error_message = f"Input validation error: {str(e)}"
        print(f"ERROR: {error_message}")
        return jsonify({"error": error_message}), 400
    except Exception as e:
        error_message = str(e)
        print(f"ERROR: Prediction error: {error_message}")
        return jsonify({"error": error_message}), 500

@app.route('/symptoms', methods=['GET'])
def list_symptoms():
    try:
        # Get all available symptoms from the dataset
        data = pd.read_csv(os.path.join(project_root, "data", "processed", "cleaned_data.csv"))
        symptom_cols = [col for col in data.columns if col != 'prognosis']
        
        return jsonify({"symptoms": symptom_cols}), 200
    
    except Exception as e:
        error_message = str(e)
        print(f"Error listing symptoms: {error_message}")
        return jsonify({"error": error_message}), 500

@app.route('/disease/<disease_name>', methods=['GET'])
def disease_info(disease_name):
    try:
        # Get top symptoms for this disease
        top_n = request.args.get('top_n', 5, type=int)
        related_symptoms = get_top_symptoms_for_disease(disease_name, top_n=top_n)
        
        if not related_symptoms:
            return jsonify({"error": f"Disease '{disease_name}' not found"}), 404
        
        return jsonify({
            "disease": disease_name,
            "top_symptoms": related_symptoms
        }), 200
    
    except Exception as e:
        error_message = str(e)
        print(f"Error getting disease info: {error_message}")
        return jsonify({"error": error_message}), 500

if __name__ == "__main__":
    try:
        print("Starting MediPredict API server...")
        
        # Check if model files exist
        if os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH):
            print(f"Model files found at: \n- {MODEL_PATH}\n- {ENCODER_PATH}")
            
            # Preload model at startup
            model, encoder = load_model()
            if model is not None and encoder is not None:
                print("✅ Model successfully preloaded and ready for predictions")
            else:
                print("⚠️ Warning: Could not preload model. Check file permissions.")
        else:
            print(f"⚠️ WARNING: Model files missing or not accessible at: \n- {MODEL_PATH}\n- {ENCODER_PATH}")
        
        # Set port and start server
        port = int(os.environ.get('PORT', 5000))
        print(f"Starting server on port {port}...")
        app.run(host='0.0.0.0', port=port, debug=False)  # Set debug=False for stability
    except Exception as e:
        print(f"Error starting Flask app: {e}")
        sys.exit(1)
