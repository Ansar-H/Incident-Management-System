"""
Configuration module for the Incident Management System.
Separates configuration for different environments (development, testing, production).
Implements security best practices for sensitive data management.
"""

import os
from datetime import timedelta

# Get the base directory (project root)
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration class with common settings."""
    
    # Flask core settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Session security settings (OWASP A07:2021 - Authentication)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # CSRF Protection (OWASP A01:2021 - Broken Access Control)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    
    # Logging configuration
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', 'False') == 'True'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Application-specific settings
    INCIDENTS_PER_PAGE = 20
    DUPLICATE_THRESHOLD = 0.85


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False
    # Use absolute path for Windows compatibility
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'incidents_dev.db')


class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'incidents_test.db')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'incidents_prod.db')
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'


# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}