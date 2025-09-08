import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from src.utils.helpers import logging, CustomException

def load_data(data_path):
    try:
        df = pd.read_csv(data_path)
        logging.info(f"Loaded data from {data_path} with shape {df.shape}")
        return df
    except Exception as e:
        raise CustomException(f"Error loading data from {data_path}: {e}")

def clean_data(df):
    try:
        # Remove the unnamed column if it exists
        if 'Unnamed: 133' in df.columns:
            df = df.drop(columns=['Unnamed: 133'])
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        logging.info(f"Cleaned data with shape {df.shape}")
        return df
    except Exception as e:
        raise CustomException(f"Error cleaning data: {e}")

def prepare_features_target(data):
    try:
        X = data.drop("prognosis", axis=1)
        y = data["prognosis"]
        return X, y
    except Exception as e:
        raise CustomException(f"Error preparing features and target: {e}")

def encode_labels(y):
    try:
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        return y_encoded, le
    except Exception as e:
        raise CustomException(f"Error encoding labels: {e}")

def split_dataset(X, y, test_size=0.2):
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=42,
            stratify=y
        )
        logging.info(f"Data split: train size {X_train.shape}, test size {X_test.shape}")
        return X_train, X_test, y_train, y_test
    except Exception as e:
        raise CustomException(f"Error splitting dataset: {e}")

def save_processed_data(df, output_path):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        logging.info(f"Processed data saved to {output_path}")
    except Exception as e:
        raise CustomException(f"Error saving processed data: {e}")
