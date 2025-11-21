"""
PyTest configuration and fixtures.
Provides reusable test setup including test client and database.
"""

import pytest
from flask import Flask
from app import db
from app.models.user import User
from app.models.incident import Incident
from werkzeug.security import generate_password_hash
from config import Config


@pytest.fixture
def app():
    """Create and configure test application."""
    # Create Flask app directly
    test_app = Flask(__name__)
    
    # Configure for testing
    test_app.config['TESTING'] = True
    test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    test_app.config['WTF_CSRF_ENABLED'] = False
    test_app.config['SECRET_KEY'] = 'test-secret-key'
    test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialise extensions
    db.init_app(test_app)
    
    with test_app.app_context():
        # Create all tables
        db.create_all()
        
        # Create test users
        testuser = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('TestPass123!'),
            is_admin=False
        )
        db.session.add(testuser)
        
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('AdminPass123!'),
            is_admin=True
        )
        db.session.add(admin)
        
        incident_user = User(
            username='incidentuser',
            email='incident@example.com',
            password_hash=generate_password_hash('Pass123!'),
            is_admin=False
        )
        db.session.add(incident_user)
        db.session.commit()
        
        # Create sample incident
        incident = Incident(
            title='Test incident for unit testing',
            platform='Additiv',
            journey='Login',
            clients_affected=5,
            description='This is a test incident created for automated testing purposes.',
            priority='Medium',
            assigned_team='LCM',
            status='Open',
            created_by=incident_user.id
        )
        db.session.add(incident)
        db.session.commit()
        
        yield test_app
        
        # Cleanup
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client for making requests."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Test CLI runner."""
    return app.test_cli_runner()

@pytest.fixture
def sample_incident(app):
    """Get the sample incident created in app fixture."""
    with app.app_context():
        incident = Incident.query.filter_by(
            title='Test incident for unit testing'
        ).first()
        return incident