"""
Authentication routes (login, logout).
Implements secure session management (OWASP A07:2021).
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.models.user import User
from app.forms.auth_forms import LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route with CSRF protection.
    Validates credentials and creates secure session.
    """
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        # Query user by username (using ORM to prevent SQL injection)
        user = User.query.filter_by(username=form.username.data).first()
        
        # Verify user exists and password is correct
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        
        # Login user with Flask-Login (creates secure session)
        login_user(user, remember=form.remember_me.data)
        
        flash(f'Welcome back, {user.username}!', 'success')
        
        # Redirect to next page or dashboard
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('main.dashboard'))
    
    return render_template('auth/login.html', title='Login', form=form)


@bp.route('/logout')
def logout():
    """Logout route - destroys session."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))