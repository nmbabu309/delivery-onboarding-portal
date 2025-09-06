from app import create_app
from extensions import db
from models import User

def check_admin():
    app = create_app()
    
    with app.app_context():
        # Check all users
        users = User.query.all()
        print("All users in database:")
        for user in users:
            print(f"- Username: {user.username}, Email: {user.email}, Role: {user.role}")
        
        # Check specifically for admin users
        admin_users = User.query.filter_by(role='admin').all()
        print(f"\nAdmin users found: {len(admin_users)}")
        for admin in admin_users:
            print(f"- Admin: {admin.username}")

if __name__ == '__main__':
    check_admin()
