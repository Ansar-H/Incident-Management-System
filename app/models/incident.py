"""
Incident model for tracking support tickets.
Stores incident details with foreign key to User (creator).
"""

from app import db
from datetime import datetime


class Incident(db.Model):
    """Incident model for helpline support tickets."""
    
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Business fields
    platform = db.Column(db.String(50), nullable=False)  # Additiv, Avaloq
    journey = db.Column(db.String(100), nullable=False)  # e.g., "Login", "Transfer"
    clients_affected = db.Column(db.Integer, default=1)
    
    # Classification
    priority = db.Column(db.String(10), nullable=False)  # P1, P2, P3, P4
    assigned_team = db.Column(db.String(50), nullable=False)  # LCM, DevOps, etc.
    status = db.Column(db.String(20), default='Open', nullable=False)  # Open, In Progress, Resolved
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)
    
    # Foreign key to user who created the incident
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Incident {self.id}: {self.title[:30]}>'