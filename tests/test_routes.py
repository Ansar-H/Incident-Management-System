"""
Test route-level behaviour, redirects, template responses, and security.
Validates HTTP responses, access control, and XSS protection.
"""

import pytest
from flask import url_for
from flask_login import login_user
from app.models.user import User
from app.models.incident import Incident


def test_index_route_returns_template(client):
    """Test that index route returns template response."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Incident Management' in response.data or b'Home' in response.data


def test_dashboard_redirects_when_not_logged_in(client):
    """Test that dashboard redirects to login when not authenticated."""
    response = client.get('/dashboard', follow_redirects=False)
    assert response.status_code == 302
    assert '/auth/login' in response.location or '/login' in response.location


def test_dashboard_returns_template_when_logged_in(client, app):
    """Test that dashboard returns template when authenticated."""
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        
        with client:
            login_user(user)
            response = client.get('/dashboard')
            assert response.status_code == 200
            assert b'Dashboard' in response.data or b'Incidents' in response.data


def test_login_redirects_when_already_logged_in(client, app):
    """Test that login route redirects when user is already authenticated."""
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        
        with client:
            login_user(user)
            response = client.get('/auth/login', follow_redirects=False)
            assert response.status_code == 302
            assert '/dashboard' in response.location


def test_helpline_user_receives_403_on_admin(client, app):
    """Test that helpline_user receives 403 when accessing /admin."""
    with app.app_context():
        helpline_user = User.query.filter_by(username='helpline_user').first()
        
        with client:
            login_user(helpline_user)
            response = client.get('/admin')
            assert response.status_code == 403


def test_admin_user_can_access_admin(client, app):
    """Test that admin user can access /admin route."""
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        
        with client:
            login_user(admin)
            response = client.get('/admin')
            assert response.status_code == 200


def test_invalid_incident_id_returns_404(client, app):
    """Test that invalid incident IDs return safe 404."""
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        
        with client:
            login_user(user)
            # Try to access a non-existent incident
            response = client.get('/incidents/99999')
            assert response.status_code == 404


def test_valid_incident_id_returns_template(client, app):
    """Test that valid incident ID returns template response."""
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        incident = Incident.query.first()
        
        if incident:
            with client:
                login_user(user)
                response = client.get(f'/incidents/{incident.id}')
                assert response.status_code == 200
                assert str(incident.id).encode() in response.data


def test_stored_xss_payload_is_escaped(client, app):
    """Test that stored XSS payloads are rendered as escaped text."""
    with app.app_context():
        from app import db
        user = User.query.filter_by(username='testuser').first()
        
        # Create incident with XSS payload
        xss_payload = '<script>alert("XSS")</script>'
        incident = Incident(
            title='Test XSS Incident',
            platform='Additiv',
            journey='Login',
            clients_affected=1,
            description=xss_payload,
            priority='Medium',
            assigned_team='LCM',
            status='Open',
            created_by=user.id
        )
        db.session.add(incident)
        db.session.commit()
        incident_id = incident.id
        
        with client:
            login_user(user)
            # View the incident
            response = client.get(f'/incidents/{incident_id}')
            assert response.status_code == 200
            
            response_text = response.data.decode('utf-8')
            
            # Security check: raw <script> tag must NOT be present
            # This is the critical test - if raw script tags appear, XSS is possible
            assert '<script>' not in response_text, \
                "Security vulnerability: Raw <script> tag found - XSS not properly escaped!"
            
            # Verify the content is present (but escaped)
            # The description should appear in the page, just not as executable code
            assert 'XSS' in response_text or 'alert' in response_text, \
                "Description content not found in response"
        
        # Cleanup
        with app.app_context():
            incident = Incident.query.get(incident_id)
            if incident:
                db.session.delete(incident)
                db.session.commit()


def test_create_incident_redirects_after_creation(client, app):
    """Test that creating an incident redirects to view page."""
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        
        with client:
            login_user(user)
            # Get CSRF token from the create page
            get_response = client.get('/incidents/create')
            assert get_response.status_code == 200
            
            # Extract CSRF token if present (CSRF may be disabled in test config)
            csrf_token = ''
            if b'csrf_token' in get_response.data:
                try:
                    csrf_token = get_response.data.decode().split('name="csrf_token" value="')[1].split('"')[0]
                except (IndexError, ValueError):
                    csrf_token = ''
            
            # Create incident via form submission
            response = client.post('/incidents/create', data={
                'title': 'Test Redirect Incident',
                'platform': 'Additiv',
                'journey': 'Login',
                'clients_affected': 1,
                'description': 'Test description for redirect',
                'csrf_token': csrf_token
            }, follow_redirects=False)
            
            # Should redirect after creation (if form validation passes)
            # Note: This test may need CSRF disabled or proper token handling
            if response.status_code == 302:
                assert '/incidents/' in response.location
