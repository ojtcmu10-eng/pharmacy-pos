from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@csrf_exempt
def create_admin_view(request):
    """One-time setup view to create admin user. DELETE AFTER USE!"""
    if User.objects.filter(username='admin').exists():
        return HttpResponse("Admin user already exists. You can delete this view now.")
    
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        role='ADMIN'
    )
    return HttpResponse("✅ Admin user created! Username: admin, Password: admin123<br><br>Now go to your app and login.<br><br><strong>IMPORTANT: Delete core/setup.py and the URL after logging in!</strong>")
