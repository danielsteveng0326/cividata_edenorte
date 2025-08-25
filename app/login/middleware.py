from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
import os

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_created = False

    def __call__(self, request):
        # Crear admin una sola vez
        if not self.admin_created and os.environ.get('RAILWAY_ENVIRONMENT'):
            self.create_admin()
            self.admin_created = True
        
        # Resto del middleware de login...
        public_urls = ['/login/', '/admin/login/', '/admin/', '/static/', '/media/']
        is_public = any(request.path.startswith(url) for url in public_urls)
        
        if not is_public and not request.user.is_authenticated:
            login_url = '/login/'
            return HttpResponseRedirect(f"{login_url}?next={request.path}")
        
        response = self.get_response(request)
        return response
    
    def create_admin(self):
        try:
            from django.contrib.auth.models import User
            
            username = 'gerencia'
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    email='edenorte@yarumal.gov.co',
                    password='NosUne.2025!',
                    first_name='Gerencia',
                    last_name='Edenorte',
                    is_staff=True,
                    is_superuser=True
                )
                print(f'✅ Usuario {username} creado desde middleware!')
        except Exception as e:
            print(f'⚠️ Error en middleware: {e}')

    