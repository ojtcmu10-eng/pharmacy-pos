from django.urls import path
from .views import (
    ProductListView, ProductCreateView, BatchCreateView, 
    InventoryIndexView, CategoryListView, CategoryCreateView,
    BatchCreateStandaloneView, BatchListView,
    ProductUpdateView, BatchUpdateView
)

urlpatterns = [
    path('', InventoryIndexView.as_view(), name='inventory_index'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/add-batch/', BatchCreateView.as_view(), name='add_batch'),
    
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    
    path('batches/', BatchListView.as_view(), name='batch_list'),
    path('batches/add/', BatchCreateStandaloneView.as_view(), name='batch_add'),
    path('batches/<int:pk>/edit/', BatchUpdateView.as_view(), name='batch_edit'),
]
