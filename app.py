"""
Application entry point for the Incident Management System.
This file runs the Flask development server.
For production deployment, use WSGI server (Gunicorn) instead.
"""

import os
from app import create_app, db

# Determine configuration environment from .env file
config_name = os.environ.get('FLASK_ENV', 'development')

# Create Flask application instance using app factory
app = create_app(config_name)

if __name__ == '__main__':
    # Ensure database tables are created
    with app.app_context():
        db.create_all()
    
    # Run development server
    # In production, use: gunicorn -w 4 -b 0.0.0.0:5000 app:app
    app.run(
        host='0.0.0.0',      # Allow external connections
        port=5000,           # Default Flask port
        debug=app.config['DEBUG']
    )