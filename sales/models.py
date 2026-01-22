from django.db import models
from django.conf import settings
from inventory.models import Batch, Product

class SaleRecord(models.Model):
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    customer_name = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=50, default='Cash')

    def __str__(self):
        return f"Sale #{self.pk} - {self.date_created.strftime('%Y-%m-%d')}"

class SaleItem(models.Model):
    sale_record = models.ForeignKey(SaleRecord, on_delete=models.CASCADE, related_name='items')
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)
