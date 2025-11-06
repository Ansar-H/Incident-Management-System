"""Routes package initialisation."""

from app.routes.auth import bp as auth_bp
from app.routes.main import bp as main_bp

__all__ = ['auth_bp', 'main_bp']