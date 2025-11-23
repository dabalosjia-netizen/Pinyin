from django.shortcuts import render
from django.http import JsonResponse
from .models import Item
from django.views.decorators.csrf import csrf_exempt

def scanner_view(request):
    return render(request, 'scanner/scanner.html')

@csrf_exempt  # for testing, remove for production and use proper CSRF
def scan_api(request):
    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        if not barcode:
            return JsonResponse({'success': False, 'error': 'No barcode provided'})
        item, created = Item.objects.get_or_create(
            barcode=barcode, 
            defaults={'name': 'Unknown Item', 'quantity': 1}
        )
        if not created:
            item.quantity += 1
            item.save()
        return JsonResponse({'success': True, 'barcode': barcode, 'name': item.name, 'quantity': item.quantity})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
