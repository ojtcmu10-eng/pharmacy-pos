from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
from .models import SaleRecord, SaleItem
from inventory.models import Product, Batch

class DailySalesListView(LoginRequiredMixin, ListView):
    model = SaleRecord
    template_name = 'sales/daily_sales.html'
    context_object_name = 'sales'

    def get_queryset(self):
        # Filter by today
        today = timezone.now().date()
        return SaleRecord.objects.filter(date_created__date=today).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculate total sales for today
        sales = self.get_queryset()
        total = sum(s.total for s in sales)
        context['total_sales'] = total
        return context

@transaction.atomic
def add_sale_view(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_ids[]')
        quantities = request.POST.getlist('quantities[]')
        customer_name = request.POST.get('customer_name')
        payment_method = request.POST.get('payment_method')

        if not product_ids:
            messages.error(request, "No items in sale record.")
            return redirect('add_sale')

        try:
            sale = SaleRecord.objects.create(
                cashier=request.user,
                customer_name=customer_name,
                payment_method=payment_method
            )
            
            total_amount = 0

            for pid, qty in zip(product_ids, quantities):
                qty = int(qty)
                product = Product.objects.get(id=pid)
                
                # Check total stock first
                if product.total_stock < qty:
                     raise ValueError(f"Insufficient stock for {product.name}")

                # FEFO
                batches = Batch.objects.filter(product=product, quantity__gt=0).order_by('expiry_date')
                
                needed = qty
                for batch in batches:
                    if needed <= 0:
                        break
                    
                    take = min(needed, batch.quantity)
                    
                    SaleItem.objects.create(
                        sale_record=sale,
                        batch=batch,
                        quantity=take,
                        price_at_sale=batch.selling_price,
                        item_total=take * batch.selling_price
                    )
                    
                    batch.quantity -= take
                    batch.save()
                    
                    total_amount += take * batch.selling_price
                    needed -= take
                
                if needed > 0:
                     raise ValueError(f"Stock mismatch error for {product.name}")

            sale.subtotal = total_amount
            sale.total = total_amount 
            sale.save()
            
            messages.success(request, "Sale Record Saved Successfully!")
            return redirect('daily_sales')

        except ValueError as e:
            # Transaction rolls back automatically due to atomic + raised exception (handled by Django?) 
            # Actually standard atomic rollback happens on exception.
            messages.error(request, str(e))
        except Exception as e:
             messages.error(request, f"An error occurred: {str(e)}")
    
    products = Product.objects.all()
    return render(request, 'sales/pos.html', {'products': products})
