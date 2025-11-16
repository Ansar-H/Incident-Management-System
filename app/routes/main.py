"""
Main application routes (homepage, about, etc.).
"""

from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('main', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    """Homepage - public access."""
    return render_template('index.html', title='Home')


@bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - requires login."""
    from app.models.incident import Incident
    
    # Get incident counts by priority
    total_incidents = Incident.query.count()
    high_priority = Incident.query.filter_by(priority='High').count()
    medium_priority = Incident.query.filter_by(priority='Medium').count()
    low_priority = Incident.query.filter_by(priority='Low').count()
    
    return render_template(
        'dashboard.html',
        title='Dashboard',
        total_incidents=total_incidents,
        high_priority=high_priority,
        medium_priority=medium_priority,
        low_priority=low_priority
    )