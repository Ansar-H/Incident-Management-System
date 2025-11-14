"""
Incident management routes (CRUD operations).
Handles incident creation, viewing, editing, and deletion.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.incident import Incident
from app.utils.decorators import admin_required

bp = Blueprint('incidents', __name__, url_prefix='/incidents')


@bp.route('/')
@bp.route('/list')
@login_required
def list_incidents():
    """
    Display list of all incidents with optional filtering.
    Accessible to all authenticated users.
    """
    # Get filter parameter from URL (e.g., ?priority=High)
    priority_filter = request.args.get('priority', None)
    
    # Query incidents
    if priority_filter:
        incidents = Incident.query.filter_by(priority=priority_filter).order_by(
            Incident.created_at.desc()
        ).all()
    else:
        incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    
    # Get count by priority for filter badges
    high_count = Incident.query.filter_by(priority='High').count()
    medium_count = Incident.query.filter_by(priority='Medium').count()
    low_count = Incident.query.filter_by(priority='Low').count()
    
    return render_template(
        'incidents/list.html',
        incidents=incidents,
        priority_filter=priority_filter,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count,
        title='All Incidents'
    )


@bp.route('/<int:id>')
@login_required
def view_incident(id):
    """
    View detailed information about a specific incident.
    Accessible to all authenticated users.
    """
    incident = Incident.query.get_or_404(id)
    
    return render_template(
        'incidents/detail.html',
        incident=incident,
        title=f'Incident #{incident.id}'
    )

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_incident():
    """
    Create a new incident with automatic priority and team assignment.
    Accessible to all authenticated users.
    """
    from app.forms.incident_forms import IncidentForm
    from app.utils.classifier import predict_priority
    from app.utils.router import assign_team
    
    form = IncidentForm()
    
    if form.validate_on_submit():
        # Automatic priority prediction
        predicted_priority = predict_priority(
            platform=form.platform.data,
            journey=form.journey.data,
            clients_affected=form.clients_affected.data,
            description=form.description.data
        )
        
        # Automatic team assignment
        assigned_team = assign_team(
            platform=form.platform.data,
            journey=form.journey.data,
            description=form.description.data
        )
        
        # Create new incident
        incident = Incident(
            title=form.title.data,
            platform=form.platform.data,
            journey=form.journey.data,
            clients_affected=form.clients_affected.data,
            description=form.description.data,
            priority=predicted_priority,
            assigned_team=assigned_team,
            status='Open',
            created_by=current_user.id
        )
        
        db.session.add(incident)
        db.session.commit()
        
        flash(f'Incident #{incident.id} created successfully! Priority: {predicted_priority}, Assigned to: {assigned_team}', 'success')
        return redirect(url_for('incidents.view_incident', id=incident.id))
    
    return render_template(
        'incidents/create.html',
        form=form,
        title='Create New Incident'
    )