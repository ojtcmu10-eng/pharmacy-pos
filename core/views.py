from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventory.models import Product

@login_required
def dashboard_view(request):
    # Basic logic for dashboard widgets
    # We will need to import models carefully to avoid circular deps if any
    # For now, just placeholder or basic query
    
    # Example logic for low stock (requires inventory app models to be ready)
    # We'll wrap in try-except or just pass 0 if not ready to avoid migration errors yet
    low_stock_count = 0
    try:
        # Assuming Product model has low_stock_limit and stock. 
        # But we haven't implemented Inventory models yet in code (only planned). 
        # So we comment this out or return 0 for now.
        pass
    except:
        pass

    context = {
        'low_stock_count': low_stock_count
    }
    return render(request, 'core/dashboard.html', context)
