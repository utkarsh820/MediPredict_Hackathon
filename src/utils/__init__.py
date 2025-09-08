from src.utils.helpers import CustomException, logging
from src.utils.config import load_config

# Initialize empty list for all exports
__all__ = [
    'CustomException',
    'logging',
    'load_config',
]

# Try to import visualization module - only if it exists
try:
    from src.utils.visualization import (
        plot_prediction_confidence,
        plot_related_symptoms,
        create_symptom_heatmap
    )
    
    # Add visualization functions to exports if available
    __all__.extend([
        'plot_prediction_confidence',
        'plot_related_symptoms',
        'create_symptom_heatmap'
    ])
except ImportError:
    # Visualization module not available in production environment
    pass
