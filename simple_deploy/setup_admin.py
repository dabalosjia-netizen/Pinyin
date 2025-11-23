#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    """Create admin user with credentials from environment variables"""
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    print(f"Attempting to create admin user: {username}")
    
    try:
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            print(f"Admin user '{username}' already exists")
            
            # Verify password
            if user.check_password(password):
                print("Admin user password is correct")
            else:
                print("Updating admin user password")
                user.set_password(password)
                user.save()
                print("Admin user password updated successfully")
        else:
            # Create new admin user
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f"Admin user '{username}' created successfully")
        
        return True
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return False

if __name__ == "__main__":
    success = create_admin_user()
    if success:
        print("Admin setup completed successfully")
        sys.exit(0)
    else:
        print("Admin setup failed")
        sys.exit(1)
