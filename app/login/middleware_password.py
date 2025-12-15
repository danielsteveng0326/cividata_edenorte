from django.shortcuts import redirect
from django.urls import reverse


class PasswordChangeMiddleware:
    """
    Middleware que redirige a los usuarios con contraseña temporal
    a la página de cambio de contraseña obligatorio.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            reverse('login:login'),
            reverse('login:logout'),
            reverse('login:primer_cambio_password'),
            '/static/',
            '/admin/',
        ]
    
    def __call__(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'perfil'):
                if request.user.perfil.requiere_cambio_password():
                    if not any(request.path.startswith(url) for url in self.exempt_urls):
                        return redirect('login:primer_cambio_password')
        
        response = self.get_response(request)
        return response
