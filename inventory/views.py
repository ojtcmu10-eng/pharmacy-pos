from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Product, Batch, Category

class InventoryIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/index.html'

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('category_list')

# Standalone Link for "Add Batch" that lets you choose the product
class BatchCreateStandaloneView(LoginRequiredMixin, CreateView):
    model = Batch
    fields = ['product', 'batch_number', 'expiry_date', 'quantity', 'cost_price', 'selling_price']
    template_name = 'inventory/batch_form.html'
    success_url = reverse_lazy('batch_list')

class BatchUpdateView(LoginRequiredMixin, UpdateView):
    model = Batch
    fields = ['product', 'batch_number', 'expiry_date', 'quantity', 'cost_price', 'selling_price']
    template_name = 'inventory/batch_form.html'
    success_url = reverse_lazy('batch_list')

class BatchListView(LoginRequiredMixin, ListView):
    model = Batch
    template_name = 'inventory/batch_list.html'
    context_object_name = 'batches'

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.all()

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'category', 'description', 'requires_prescription', 'low_stock_limit', 'reorder_level']
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'category', 'description', 'requires_prescription', 'low_stock_limit', 'reorder_level']
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')

class BatchCreateView(LoginRequiredMixin, CreateView):
    model = Batch
    fields = ['batch_number', 'expiry_date', 'quantity', 'cost_price', 'selling_price']
    template_name = 'inventory/batch_form.html'

    def form_valid(self, form):
        form.instance.product = get_object_or_404(Product, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(Product, pk=self.kwargs['pk'])
        return context
