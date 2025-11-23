from django.db import migrations
from django.contrib.auth.models import User
import os


def create_admin_user(apps, schema_editor):
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)


def reverse_create_admin_user(apps, schema_editor):
    User.objects.filter(username='admin').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('myproject', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin_user, reverse_create_admin_user),
    ]
