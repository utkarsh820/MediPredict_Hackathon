"""
WSGI entry point for the MediPredict application.
This file helps with proper module discovery and application loading.
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the Flask application
from src.app import app

# This is for direct execution of this file
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
