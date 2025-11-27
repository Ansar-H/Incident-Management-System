"""
Main application routes (homepage, dashboard, admin).
"""

from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

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

@bp.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard - requires admin privileges."""
    
    if not current_user.is_admin:
        abort(403)

    from app.models.incident import Incident
    from app.models.user import User
    
    # Get comprehensive statistics for admin
    total_incidents = Incident.query.count()
    high_priority = Incident.query.filter_by(priority='High').count()
    medium_priority = Incident.query.filter_by(priority='Medium').count()
    low_priority = Incident.query.filter_by(priority='Low').count()
    
    # Get status counts
    open_incidents = Incident.query.filter_by(status='Open').count()
    in_progress = Incident.query.filter_by(status='In Progress').count()
    resolved = Incident.query.filter_by(status='Resolved').count()
    closed = Incident.query.filter_by(status='Closed').count()
    
    # Get user counts
    total_users = User.query.count()
    admin_users = User.query.filter_by(is_admin=True).count()
    regular_users = User.query.filter_by(is_admin=False).count()
    
    # Get recent incidents
    recent_incidents = Incident.query.order_by(Incident.created_at.desc()).limit(10).all()
    
    return render_template(
        'admin_dashboard.html',
        title='Admin Dashboard',
        total_incidents=total_incidents,
        high_priority=high_priority,
        medium_priority=medium_priority,
        low_priority=low_priority,
        open_incidents=open_incidents,
        in_progress=in_progress,
        resolved=resolved,
        closed=closed,
        total_users=total_users,
        admin_users=admin_users,
        regular_users=regular_users,
        recent_incidents=recent_incidents,
        is_admin_dashboard=True
    )