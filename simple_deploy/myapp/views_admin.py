from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

@csrf_exempt
def test_admin_login(request):
    """Test admin login credentials"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username', 'admin')
            password = data.get('password', 'admin123')
            
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                return JsonResponse({
                    'success': True,
                    'message': 'Admin login successful',
                    'username': username,
                    'is_superuser': user.is_superuser,
                    'is_staff': user.is_staff
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid admin credentials'
                }, status=401)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=500)
    
    # GET request - show admin users
    admin_users = User.objects.filter(is_superuser=True).values('username', 'email', 'is_staff')
    return JsonResponse({
        'admin_users': list(admin_users),
        'total_admins': User.objects.filter(is_superuser=True).count()
    })
