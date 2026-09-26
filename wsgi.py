"""
wsgi.py — Entry point for production deployment
Author  : Daniel Oyanogbezina
Purpose : Tells gunicorn where to find the Flask app
          Render.com and other servers use this file
"""

import sys
import os

# Add the api/ folder to Python path
# So advisory.py and predictor.py can be found
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

from app import app          # imports Flask app from api/app.py

if __name__ == "__main__":
    app.run()