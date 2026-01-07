"""
Audit log model for tracking incident override actions.
Implements governance and traceability for admin actions.
"""

from app import db
from datetime import datetime


class AuditLog(db.Model):
    """
    Tracks all override actions performed by admins.
    Part of OWASP A09:2021 - Security Logging and Monitoring.
    """
    
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # What was changed
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    field_changed = db.Column(db.String(50), nullable=False)  # 'priority', 'team', or 'both'
    
    # Old and new values
    old_priority = db.Column(db.String(10), nullable=True)
    new_priority = db.Column(db.String(10), nullable=True)
    old_team = db.Column(db.String(50), nullable=True)
    new_team = db.Column(db.String(50), nullable=True)
    
    # Why it was changed
    reason_code = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    
    # Who and when
    changed_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    incident = db.relationship('Incident', backref='audit_logs')
    changed_by = db.relationship('User', backref='audit_actions')
    
    def __repr__(self):
        return f'<AuditLog {self.id}: Incident #{self.incident_id} by User #{self.changed_by_user_id}>'