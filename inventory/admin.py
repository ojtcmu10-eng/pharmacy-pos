from django.contrib import admin
from .models import Category, Product, Batch

class BatchInline(admin.TabularInline):
    model = Batch
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'total_stock', 'requires_prescription')
    inlines = [BatchInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Batch)
