"""
Authentication forms with WTForms validation.
Includes CSRF protection (OWASP A01:2021 - Broken Access Control).
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Login form with username and password fields."""
    
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=64, message='Username must be between 3 and 64 characters')
        ]
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required'),
            Length(min=6, message='Password must be at least 6 characters')
        ]
    )
    
    remember_me = BooleanField('Remember Me')
    
    submit = SubmitField('Login')