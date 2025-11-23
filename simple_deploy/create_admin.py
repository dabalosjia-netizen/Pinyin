#!/usr/bin/env python
"""
Robust admin user creation script for Django deployment
"""

import os
import sys
import django

def main():
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Setup Django
    try:
        django.setup()
        print("Django setup successful")
    except Exception as e:
        print(f"Django setup failed: {e}")
        return False
    
    # Import Django models after setup
    try:
        from django.contrib.auth.models import User
        print("Django models imported successfully")
    except Exception as e:
        print(f"Failed to import Django models: {e}")
        return False
    
    # Get admin credentials from environment
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    print(f"Creating admin user: {username}")
    print(f"Email: {email}")
    print(f"Password: {'*' * len(password)}")
    
    try:
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            print(f"Admin user '{username}' already exists")
            
            # Verify and update password if needed
            if user.check_password(password):
                print("✅ Admin user password is correct")
            else:
                print("🔄 Updating admin user password...")
                user.set_password(password)
                user.is_superuser = True
                user.is_staff = True
                user.save()
                print("✅ Admin user password updated successfully")
        else:
            # Create new admin user
            print("🔄 Creating new admin user...")
            user = User.objects.create_superuser(username=username, email=email, password=password)
            print(f"✅ Admin user '{username}' created successfully")
        
        # Verify the user is properly configured
        user = User.objects.get(username=username)
        if user.is_superuser and user.is_staff:
            print("✅ Admin user has superuser and staff privileges")
            return True
        else:
            print("❌ Admin user missing privileges - fixing...")
            user.is_superuser = True
            user.is_staff = True
            user.save()
            print("✅ Admin user privileges fixed")
            return True
            
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Django Admin User Creation Script")
    print("=" * 50)
    
    success = main()
    
    print("=" * 50)
    if success:
        print("🎉 Admin setup completed successfully!")
        print(f"Login URL: https://pinyin-cdaz.onrender.com/admin")
        print(f"Username: admin")
        print(f"Password: admin123")
        sys.exit(0)
    else:
        print("💥 Admin setup failed!")
        sys.exit(1)
