"""
Main application routes (homepage, about, etc.).
"""

from flask import Blueprint, render_template
from flask_login import login_required

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
    return render_template('dashboard.html', title='Dashboard')