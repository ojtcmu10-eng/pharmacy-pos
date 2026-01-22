from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Sum, Count, F
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from sales.models import SaleRecord, SaleItem
from inventory.models import Product
import datetime
import json

class ReportsIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localtime().date()
        
        # --- Totals ---
        daily_sales = SaleRecord.objects.filter(date_created__date=today).aggregate(t=Sum('total'))['t'] or 0
        monthly_sales = SaleRecord.objects.filter(date_created__month=today.month, date_created__year=today.year).aggregate(t=Sum('total'))['t'] or 0
        
        # --- Charts Data ---
        # 1. Sales Over Time (Last 30 Days)
        last_30_days = today - datetime.timedelta(days=30)
        sales_data = (
            SaleRecord.objects.filter(date_created__date__gte=last_30_days)
            .values('date_created__date')
            .annotate(total_sales=Sum('total'))
            .order_by('date_created__date')
        )
        
        # Prepare for Chart.js
        dates = [entry['date_created__date'].strftime('%Y-%m-%d') for entry in sales_data]
        amounts = [float(entry['total_sales']) for entry in sales_data]
        
        # 2. Top Selling Products
        top_products = (
            SaleItem.objects.all()
            .values('batch__product__name')
            .annotate(qty_sold=Sum('quantity'))
            .order_by('-qty_sold')[:5]
        )
        
        prod_names = [entry['batch__product__name'] for entry in top_products]
        prod_qtys = [entry['qty_sold'] for entry in top_products]

        # --- Detailed Report Filtering ---
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        product_id = self.request.GET.get('product_id')
        
        # Base Query
        detailed_items = SaleItem.objects.all().select_related('sale_record', 'batch__product', 'sale_record__cashier').order_by('-sale_record__date_created')
        
        # Apply Filters
        if start_date:
            detailed_items = detailed_items.filter(sale_record__date_created__date__gte=start_date)
        if end_date:
            detailed_items = detailed_items.filter(sale_record__date_created__date__lte=end_date)
        if product_id:
            detailed_items = detailed_items.filter(batch__product_id=product_id)

        # Context Updates
        context.update({
            'daily_sales_total': daily_sales,
            'monthly_sales_total': monthly_sales,
            'chart_dates': json.dumps(dates),
            'chart_sales': json.dumps(amounts),
            'top_prod_names': json.dumps(prod_names),
            'top_prod_qtys': json.dumps(prod_qtys),
            # Detailed Report Context
            'detailed_items': detailed_items,
            'all_products': Product.objects.all().order_by('name'),
            'filter_start': start_date,
            'filter_end': end_date,
            'filter_product_id': int(product_id) if product_id else '',
        })
        return context
