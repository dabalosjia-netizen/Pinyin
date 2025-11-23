from django.db import models

class Item(models.Model):
    barcode = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    last_scanned = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.barcode})"
