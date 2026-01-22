from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    requires_prescription = models.BooleanField(default=False)
    low_stock_limit = models.IntegerField(default=10)
    reorder_level = models.IntegerField(default=20)

    def __str__(self):
        return self.name
        
    @property
    def total_stock(self):
        return sum(batch.quantity for batch in self.batch_set.all())

class Batch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=50)
    expiry_date = models.DateField()
    quantity = models.IntegerField(default=0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.batch_number}"
