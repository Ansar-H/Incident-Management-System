"""
Custom decorators for access control.
Implements RBAC (OWASP A01:2021 - Broken Access Control).
"""

from functools import wraps
from flask import abort
from flask_login import current_user


def admin_required(f):
    """
    Decorator to restrict access to admin users only.
    
    Usage:
        @app.route('/admin/dashboard')
        @login_required
        @admin_required
        def admin_dashboard():
            return render_template('admin/dashboard.html')
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)  # Forbidden
        if not current_user.is_admin:
            abort(403)  # Forbidden - user is logged in but not admin
        return f(*args, **kwargs)
    return decorated_function