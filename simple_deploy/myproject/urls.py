from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myapp import views
from myapp import views_debug
from myapp import views_admin

urlpatterns = [
    path('admin/', admin.site.urls),

    # Include your app URLs first
    path('', include('myapp.urls')),

    # Scanner
    path('scanner/', views.scanner_view, name='scanner'),

    # Products
    path('products/', views.get_products, name='get_products'),
    
    # Debug endpoints
    path('debug/users/', views_debug.check_users, name='check_users'),
    path('test-admin/', views_admin.test_admin_login, name='test_admin_login'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
