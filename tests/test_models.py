"""
Test database models.
Validates User and Incident model functionality.
"""

from app.models.user import User
from app.models.incident import Incident
from app import db
from werkzeug.security import generate_password_hash


def test_user_password_hashing(app):
    """Test password hashing and verification."""
    user = User(username='hashtest', email='hash@test.com')
    user.set_password('SecurePass123!')
    
    assert user.password_hash is not None
    assert user.password_hash != 'SecurePass123!'
    assert user.check_password('SecurePass123!') is True
    assert user.check_password('WrongPassword') is False


def test_user_creation(app):
    """Test user can be created and saved to database."""
    user = User(
        username='newuser',
        email='new@test.com',
        password_hash=generate_password_hash('NewPass123!'),
        is_admin=False
    )
    
    db.session.add(user)
    db.session.commit()
    
    retrieved = User.query.filter_by(username='newuser').first()
    assert retrieved is not None
    assert retrieved.email == 'new@test.com'
    assert retrieved.is_admin is False


def test_incident_creation(app):
    """Test incident can be created with all required fields."""
    incident = Incident.query.filter_by(title='Test incident for unit testing').first()
    
    assert incident is not None
    assert incident.platform == 'Additiv'
    assert incident.priority == 'Medium'
    assert incident.status == 'Open'


def test_incident_relationship(app):
    """Test incident-user relationship works correctly."""
    incident = Incident.query.filter_by(title='Test incident for unit testing').first()
    
    assert incident.creator is not None
    assert incident.creator.username == 'incidentuser'


def test_incident_timestamps(app):
    """Test incident has created_at timestamp."""
    incident = Incident.query.filter_by(title='Test incident for unit testing').first()
    
    assert incident.created_at is not None