from django.urls import path
from .views import DailySalesListView, add_sale_view

urlpatterns = [
    path('', DailySalesListView.as_view(), name='daily_sales'),
    path('add/', add_sale_view, name='add_sale'),
]
