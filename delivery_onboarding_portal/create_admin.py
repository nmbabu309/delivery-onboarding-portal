from app import create_app
from extensions import db
from models import User

def create_admin_user():
    app = create_app()
    
    with app.app_context():
        # Check if admin exists
        existing_admin = User.query.filter_by(role='admin').first()
        if existing_admin:
            print(f"Admin already exists: {existing_admin.username}")
            return
        
        # Create admin with custom credentials
        admin = User(
            username='admin',  # Change this
            email='admin@gmail.com',  # Change this
            role='admin'
        )
        admin.set_password('admin123')  # Change this
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Admin user created!")
        print(f"Username: your_username")
        print(f"Password: your_password")

if __name__ == '__main__':
    create_admin_user()
