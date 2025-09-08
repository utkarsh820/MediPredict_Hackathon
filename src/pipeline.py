import os
from src.data.preprocess import (
    load_data, 
    clean_data, 
    prepare_features_target,
    encode_labels,
    split_dataset,
    save_processed_data
)
from src.models.train import (
    train_catboost_model,
    evaluate_model,
    save_model,
    save_feature_names
)
from src.utils.helpers import logging, CustomException

def run_training_pipeline(data_path=None):
    try:
        # Set default data path if not provided
        if data_path is None:
            data_path = 'data/processed/cleaned_data.csv'
        
        # Load and prepare data
        logging.info("Loading data...")
        data = load_data(data_path)
        
        # Prepare model inputs
        logging.info("Preparing features and target...")
        X, y = prepare_features_target(data)
        y_encoded, le = encode_labels(y)
        
        # Split data
        logging.info("Splitting dataset...")
        X_train, X_test, y_train, y_test = split_dataset(X, y_encoded)
        
        # Train CatBoost model
        logging.info("Training CatBoost model...")
        model = train_catboost_model(X_train, y_train)
        
        # Evaluate model
        logging.info("Evaluating model...")
        results = evaluate_model(model, X_test, y_test)
        
        # Save model and feature names
        logging.info("Saving model...")
        save_model(model, le)
        save_feature_names(list(X.columns))
        
        logging.info(f"Pipeline completed. Model accuracy: {results['accuracy']:.4f}")
        
        return {
            'model': model,
            'results': results,
            'accuracy': results['accuracy']
        }
    except Exception as e:
        raise CustomException(f"Error in training pipeline: {e}")

if __name__ == "__main__":
    try:
        run_training_pipeline()
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise
