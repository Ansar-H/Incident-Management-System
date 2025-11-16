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
    from flask_wtf import FlaskForm
    
    incident = Incident.query.get_or_404(id)
    form = FlaskForm()  # Create empty form just for CSRF token
    
    return render_template(
        'incidents/detail.html',
        incident=incident,
        form=form,  # Pass form to template
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

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_incident(id):
    """
    Edit an existing incident.
    Users can edit their own incidents, admins can edit any incident.
    """
    from app.forms.incident_forms import IncidentForm
    from app.utils.classifier import predict_priority
    from app.utils.router import assign_team
    
    incident = Incident.query.get_or_404(id)
    
    # Check permissions: users can edit their own, admins can edit any
    if not current_user.is_admin and incident.created_by != current_user.id:
        flash('You do not have permission to edit this incident.', 'danger')
        return redirect(url_for('incidents.list_incidents'))
    
    form = IncidentForm()
    
    if form.validate_on_submit():
        # Update incident fields
        incident.title = form.title.data
        incident.platform = form.platform.data
        incident.journey = form.journey.data
        incident.clients_affected = form.clients_affected.data
        incident.description = form.description.data
        
        # Recalculate priority and team based on updated data
        incident.priority = predict_priority(
            platform=form.platform.data,
            journey=form.journey.data,
            clients_affected=form.clients_affected.data,
            description=form.description.data
        )
        
        incident.assigned_team = assign_team(
            platform=form.platform.data,
            journey=form.journey.data,
            description=form.description.data
        )
        
        db.session.commit()
        
        flash(f'Incident #{incident.id} updated successfully! Priority: {incident.priority}, Assigned to: {incident.assigned_team}', 'success')
        return redirect(url_for('incidents.view_incident', id=incident.id))
    
    # Pre-populate form with existing data
    if request.method == 'GET':
        form.title.data = incident.title
        form.platform.data = incident.platform
        form.journey.data = incident.journey
        form.clients_affected.data = incident.clients_affected
        form.description.data = incident.description
    
    return render_template(
        'incidents/edit.html',
        form=form,
        incident=incident,
        title=f'Edit Incident #{incident.id}'
    )


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_incident(id):
    """
    Delete an incident (admin only).
    Uses POST method to prevent CSRF attacks.
    """
    incident = Incident.query.get_or_404(id)
    
    incident_id = incident.id
    db.session.delete(incident)
    db.session.commit()
    
    flash(f'Incident #{incident_id} has been deleted successfully.', 'success')
    return redirect(url_for('incidents.list_incidents'))