from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def check_users(request):
    users = list(User.objects.values('username', 'email', 'is_superuser', 'is_staff'))
    return JsonResponse({
        'total_users': User.objects.count(),
        'admin_users': User.objects.filter(is_superuser=True).count(),
        'users': users
    })
