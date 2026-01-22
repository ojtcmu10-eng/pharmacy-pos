from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class UserLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')

class UserLogoutView(LogoutView):
    next_page = 'login'
    
    # Custom: Allow GET for logout (since Django 5.0+ defaults to POST-only)
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
