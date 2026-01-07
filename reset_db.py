"""
This is a database reset script - FOR DEVELOPMENT ONLY
Drops all tables and recreates them with the new schema.
"""

from app import create_app, db
from app.models import User, Incident, AuditLog

def reset_database():
    """Drop all tables and recreate them."""
    app = create_app()
    
    with app.app_context():
        print("🗑️  Dropping all tables...")
        db.drop_all()
        
        print("🔨 Creating all tables with new schema...")
        db.create_all()
        
        print("✅ Database reset complete!")
        print("\n📋 Tables created:")
        print("  - users")
        print("  - incidents (with NEW fields: predicted_priority, predicted_team, duplicate_flag, duplicate_score, is_overridden)")
        print("  - audit_logs")
        
        # Create a test admin user
        from werkzeug.security import generate_password_hash
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('Admin123!'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        
        print("\n👤 Test admin user created:")
        print("  Username: admin")
        print("  Password: Admin123!")

if __name__ == '__main__':
    reset_database()