"""
Smoke tests for basic application functionality.
These are quick tests to verify core components are working.
"""

import pytest
from app import create_app, db


def test_app_creation():
    """Test that the Flask app can be created."""
    app = create_app('testing')
    assert app is not None
    assert app.config['TESTING'] is True


def test_database_connection(client):
    """Test that database connection works."""
    with client.application.app_context():
        # Try to query the database
        from app.models.user import User
        user_count = User.query.count()
        assert isinstance(user_count, int)


def test_app_index_page(client):
    """Test that the home page loads."""
    response = client.get('/')
    assert response.status_code in [200, 302]  # 302 if redirected to login


def test_test_configuration(client):
    """Test that test configuration is correct."""
    assert client.application.config['TESTING'] is True
    assert client.application.config['WTF_CSRF_ENABLED'] is False
