"""
Forms for incident override functionality.
Admin-only forms for correcting triage predictions.
"""

from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired


class OverrideForm(FlaskForm):
    """Form for admins to override triage decisions."""
    
    new_priority = SelectField(
        'New Priority',
        choices=[
            ('', '-- Select Priority --'),
            ('High', 'High'),
            ('Medium', 'Medium'),
            ('Low', 'Low')
        ],
        validators=[DataRequired(message='Please select a priority')]
    )
    
    new_team = SelectField(
        'New Team',
        choices=[
            ('', '-- Select Team --'),
            ('LCM', 'LCM'),
            ('DevOps', 'DevOps'),
            ('Additiv Support', 'Additiv Support'),
            ('Avaloq Support', 'Avaloq Support'),
            ('Platform Support', 'Platform Support')
        ],
        validators=[DataRequired(message='Please select a team')]
    )
    
    reason_code = SelectField(
        'Reason for Override',
        choices=[
            ('', '-- Select Reason --'),
            ('incorrect_platform_detection', 'Incorrect journey/platform detected'),
            ('keyword_misclassification', 'Keyword-based misclassification'),
            ('edge_case', 'Edge case / ambiguous incident'),
            ('business_impact', 'Business impact adjustment'),
            ('other', 'Other')
        ],
        validators=[DataRequired(message='Please select a reason')]
    )
    
    comment = TextAreaField(
        'Additional Comments (Optional)',
        render_kw={'rows': 3, 'placeholder': 'Provide additional context if needed...'}
    )