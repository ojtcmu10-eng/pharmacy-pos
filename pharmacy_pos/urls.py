from django.contrib import admin
from django.urls import path, include
from core.setup import create_admin_view  # Temporary setup view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('setup-admin-once/', create_admin_view, name='setup_admin'),  # DELETE AFTER USE!
    path('', include('core.urls')),
    path('auth/', include('authentication.urls')),
    path('inventory/', include('inventory.urls')),
    path('sales/', include('sales.urls')),
    path('reports/', include('reports.urls')),
]
