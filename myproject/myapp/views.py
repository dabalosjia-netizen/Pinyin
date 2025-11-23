from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ProductForm, RegisterForm
from .models import Product


def scanner_view(request):
    """Render the scanner page on GET, handle barcode lookup on POST (JSON)."""
    if request.method == "POST":
        # Expect JSON body: {"barcode": "..."}
        import json

        try:
            data = json.loads(request.body.decode("utf-8"))
            barcode = str(data.get("barcode", "")).strip()
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        if not barcode:
            return JsonResponse({"error": "Missing barcode"}, status=400)

        try:
            product = Product.objects.get(barcode=barcode)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

        return JsonResponse(
            {
                "barcode": product.barcode,
                "name": product.name,
                "price": str(product.price),
            }
        )

    # GET request: render the scanner UI
    return render(request, "scanner.html")


def home_view(request):
    return render(request, "home.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. You can now log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("scanner")
        messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def _is_staff_or_superuser(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@user_passes_test(_is_staff_or_superuser)
def admin_dashboard2(request):
    """Simple admin dashboard showing all products."""
    products = Product.objects.all().order_by("name")
    return render(request, "admin_dashboard2/dashboard2.html", {"products": products})


@user_passes_test(_is_staff_or_superuser)
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_dashboard")
    else:
        form = ProductForm()
    return render(request, "admin_dashboard2/product_form.html", {"form": form})


@user_passes_test(_is_staff_or_superuser)
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("admin_dashboard")
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        "admin_dashboard2/product_form.html",
        {"form": form, "product": product},
    )


@user_passes_test(_is_staff_or_superuser)
@require_http_methods(["POST"])
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("admin_dashboard")


@require_http_methods(["GET"])
def get_products(request):
    """Return all products as a JSON list.

    Shape: [{"id", "barcode", "name", "price", "image_url"}, ...]
    """
    products = Product.objects.all().order_by("name")
    data = []
    for p in products:
        data.append(
            {
                "id": p.id,
                "barcode": p.barcode,
                "name": p.name,
                "price": str(p.price),
                "image_url": p.image.url if p.image else None,
            }
        )
    return JsonResponse(data, safe=False)