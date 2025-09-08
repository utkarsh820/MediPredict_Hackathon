import os
import yaml
from src.utils.helpers import logging, CustomException

def load_config(config_path='config/config.yaml'):
    try:
        if not os.path.exists(config_path):
            default_config = create_default_config()
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            with open(config_path, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            
            logging.info(f"Created default config at {config_path}")
            return default_config
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        logging.info(f"Loaded config from {config_path}")
        return config
    except Exception as e:
        raise CustomException(f"Error loading config: {e}")

def create_default_config():
    return {
        'data': {
            'raw_dir': 'data/raw',
            'processed_dir': 'data/processed',
            'training_file': 'Training.csv',
            'testing_file': 'Testing.csv',
            'cleaned_file': 'cleaned_data.csv'
        },
        'models': {
            'output_dir': 'models',
            'xgb': {
                'n_estimators': 200,
                'learning_rate': 0.05,
                'max_depth': 5,
                'subsample': 0.8,
                'colsample_bytree': 0.8
            },
            'lgb': {
                'n_estimators': 200,
                'learning_rate': 0.05,
                'max_depth': -1,
                'subsample': 0.8,
                'colsample_bytree': 0.8
            },
            'cat': {
                'iterations': 200,
                'learning_rate': 0.05,
                'depth': 6
            }
        },
        'training': {
            'test_size': 0.2,
            'random_state': 42
        }
    }
