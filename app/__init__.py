"""
Flask application factory.
Creates and configures the Flask application instance with all extensions.
Implements the application factory pattern for better testing and modularity.
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialize extensions (without binding to app yet)
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name='default'):
    """
    Application factory function.
    
    Args:
        config_name (str): Configuration environment name ('development', 'testing', 'production')
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configure Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Import models here (after db is initialized) to avoid circular imports
    from app.models.user import User
    from app.models.incident import Incident
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        """Flask-Login user loader callback."""
        return User.query.get(int(user_id))
    
    # Register blueprints (routes) to the application
    from app.routes import auth_bp, main_bp, incidents_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(incidents_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Configure logging
    configure_logging(app)
    
    # Create database tables and seed data
    with app.app_context():
        db.create_all()
        initialize_database()
    
    app.logger.info('Incident Management System startup complete')
    
    return app


def register_error_handlers(app):
    """Register custom error handlers for common HTTP errors."""
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden errors (OWASP A01 - Access Control)."""
        return f"<h1>403 Forbidden</h1><p>Access denied.</p>", 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return f"<h1>404 Not Found</h1><p>The requested resource was not found.</p>", 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors."""
        db.session.rollback()
        app.logger.error(f'Internal server error: {error}')
        return f"<h1>500 Internal Server Error</h1><p>Something went wrong.</p>", 500


def configure_logging(app):
    """Configure application logging for audit trail and debugging."""
    
    if not app.debug and not app.testing:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Configure rotating file handler
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)


def initialize_database():
    """Initialize database with sample data for development/testing."""
    from app.models.user import User
    from app.models.incident import Incident
    
    # Only seed if database is empty
    if User.query.count() == 0:
        print("Seeding database with sample data...")
        
        try:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@natwest.internal',
                is_admin=True
            )
            admin.set_password('Admin123!')
            db.session.add(admin)
            
            # Create regular helpline user
            user = User(
                username='helpline_user',
                email='helpline@natwest.internal',
                is_admin=False
            )
            user.set_password('User123!')
            db.session.add(user)
            
            # Commit users first to get their IDs
            db.session.commit()
            
            # Create sample incidents
            incidents = [
                Incident(
                    title='Client cannot log into Additiv platform',
                    description='Client reports login failure with error code AUTH_TIMEOUT. Multiple retry attempts failed.',
                    platform='Additiv',
                    journey='Login',
                    clients_affected=1,
                    predicted_priority='Medium',
                    predicted_team='LCM',
                    duplicate_flag=False,
                    duplicate_score=None,
                    is_overridden=False,
                    priority='Medium',
                    assigned_team='LCM',
                    status='Open',
                    created_by=user.id
                ),
                Incident(
                    title='Data sync mismatch between Additiv and Avaloq',
                    description='Portfolio values not syncing correctly. Client balance showing £10k difference.',
                    platform='Avaloq',
                    journey='Data Sync',
                    clients_affected=5,
                    predicted_priority='High',
                    predicted_team='DevOps',
                    duplicate_flag=False,
                    duplicate_score=None,
                    is_overridden=False,
                    priority='High',
                    assigned_team='DevOps',
                    status='In Progress',
                    created_by=user.id
                ),
                Incident(
                    title='Transfer transaction failing with timeout',
                    description='Client trying to transfer £50k between accounts. Transaction times out after 30 seconds.',
                    platform='Additiv',
                    journey='Transfer',
                    clients_affected=1,
                    predicted_priority='Low',
                    predicted_team='Platform Support',
                    duplicate_flag=False,
                    duplicate_score=None,
                    is_overridden=False,
                    priority='Low',
                    assigned_team='Platform Support',
                    status='Open',
                    created_by=admin.id
                )
            ]
            
            for incident in incidents:
                db.session.add(incident)
            
            db.session.commit()
            
            print(f"✓ Created {User.query.count()} users")
            print(f"✓ Created {Incident.query.count()} sample incidents")
            print("\nDefault credentials:")
            print("  Admin: username='admin', password='Admin123!'")
            print("  User:  username='helpline_user', password='User123!'")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding database: {e}")