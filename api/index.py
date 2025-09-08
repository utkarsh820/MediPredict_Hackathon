"""
Vercel API handler for MediPredict
This file serves as the entry point for Vercel serverless functions.
It imports and initializes the Flask app.
"""
from src.app import app
import os
import sys
import importlib.util

# Try to import and use the Vercel helpers
try:
    # Add the project root to sys.path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        
    # Try to import the helper directly
    from src.utils.vercel_helpers import ensure_model_files
    
    # Check if models need to be downloaded
    ensure_model_files()
except Exception as e:
    print(f"Error importing Vercel helpers: {str(e)}")

# This is required for Vercel to recognize the app
from http.server import HTTPServer, BaseHTTPRequestHandler
handler = app
