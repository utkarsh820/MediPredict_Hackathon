"""
Vercel API handler for MediPredict
This file serves as the entry point for Vercel serverless functions.
It imports and initializes the Flask app.
"""
import os
import sys

# Add the project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import Flask app
from src.app import app

# This is required for Vercel to recognize the app
handler = app
