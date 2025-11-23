from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.admin_dashboard2, name="dashboard"),
    path("admin-dashboard/", views.admin_dashboard2, name="admin_dashboard"),
    path("admin-dashboard-2/", views.admin_dashboard2, name="admin_dashboard_2"),
    path("admin-dashboard/product/create/", views.product_create, name="product_create"),
    path("admin-dashboard/product/<int:pk>/edit/", views.product_edit, name="product_edit"),
    path("admin-dashboard/product/<int:pk>/delete/", views.product_delete, name="product_delete"),
    path("scanner/", views.scanner_view, name="scanner"),
]
