"""
Incident forms with WTForms validation.
Includes fields for incident creation and editing.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class IncidentForm(FlaskForm):
    """Form for creating and editing incidents."""
    
    title = StringField(
        'Incident Title',
        validators=[
            DataRequired(message='Title is required'),
            Length(min=10, max=200, message='Title must be between 10 and 200 characters')
        ],
        render_kw={'placeholder': 'Brief description of the issue'}
    )
    
    platform = SelectField(
        'Platform',
        choices=[
            ('Additiv', 'Additiv'),
            ('Avaloq', 'Avaloq')
        ],
        validators=[DataRequired(message='Platform is required')]
    )
    
    journey = SelectField(
        'Customer Journey',
        choices=[
            ('Login', 'Login'),
            ('Transfer', 'Transfer'),
            ('Payment', 'Payment'),
            ('Balance View', 'Balance View'),
            ('Account Access', 'Account Access'),
            ('Data Sync', 'Data Sync'),
            ('Reporting', 'Reporting'),
            ('Other', 'Other')
        ],
        validators=[DataRequired(message='Journey is required')]
    )
    
    clients_affected = IntegerField(
        'Clients Affected',
        validators=[
            DataRequired(message='Number of clients is required'),
            NumberRange(min=1, max=10000, message='Must be between 1 and 10,000')
        ],
        default=1
    )
    
    description = TextAreaField(
        'Detailed Description',
        validators=[
            DataRequired(message='Description is required'),
            Length(min=20, max=2000, message='Description must be between 20 and 2,000 characters')
        ],
        render_kw={
            'rows': 6,
            'placeholder': 'Provide detailed information about the incident, including error messages, steps to reproduce, and client impact...'
        }
    )
    
    submit = SubmitField('Create Incident')

class EditIncidentForm(IncidentForm):
    """
    Form for editing incidents.
    Inherits from IncidentForm but changes the submit button text.
    """
    submit = SubmitField('Update Incident')