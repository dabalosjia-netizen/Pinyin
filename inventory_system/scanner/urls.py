from django.urls import path
from . import views

urlpatterns = [
    path('', views.scanner_view, name='scanner'),
    path('scan/', views.scan_api, name='scan_api'),
]
