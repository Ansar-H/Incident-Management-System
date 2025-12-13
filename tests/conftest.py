"""
PyTest configuration and fixtures.
Provides reusable test setup including test client and database.
"""

import pytest
from app import create_app, db
from app.models.user import User
from app.models.incident import Incident
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Create and configure test application."""
    # Using the app factory to ensure all blueprints are registered
    test_app = create_app('testing')
    
    # Override database URI to use in-memory database for faster tests
    test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with test_app.app_context():
        # Drop all tables first (in case the app factory created them)
        db.drop_all()
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
        
        # Create helpline_user for security tests
        helpline_user = User(
            username='helpline_user',
            email='helpline@example.com',
            password_hash=generate_password_hash('Helpline123!'),
            is_admin=False
        )
        db.session.add(helpline_user)
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