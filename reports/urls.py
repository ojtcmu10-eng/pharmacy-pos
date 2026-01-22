from django.urls import path
from .views import ReportsIndexView

urlpatterns = [
    path('', ReportsIndexView.as_view(), name='reports'),
]
