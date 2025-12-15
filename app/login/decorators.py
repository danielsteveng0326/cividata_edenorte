from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden


def superuser_required(view_func):
    """
    Decorador que requiere que el usuario sea superusuario del sistema.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login:login')
        
        if hasattr(request.user, 'perfil'):
            if request.user.perfil.es_superusuario_sistema or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
        
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('index')
    
    return wrapper


def puede_gestionar_usuarios_required(view_func):
    """
    Decorador que requiere que el usuario pueda gestionar usuarios.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login:login')
        
        if hasattr(request.user, 'perfil'):
            if (request.user.perfil.es_superusuario_sistema or 
                request.user.perfil.puede_gestionar_usuarios or 
                request.user.is_superuser):
                return view_func(request, *args, **kwargs)
        
        messages.error(request, 'No tienes permisos para gestionar usuarios.')
        return redirect('index')
    
    return wrapper


def modulo_required(codigo_modulo):
    """
    Decorador que requiere acceso a un módulo específico.
    
    Uso:
        @modulo_required('paa')
        def mi_vista(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login:login')
            
            if hasattr(request.user, 'perfil'):
                if request.user.perfil.tiene_acceso_modulo(codigo_modulo):
                    return view_func(request, *args, **kwargs)
            
            messages.error(request, f'No tienes acceso al módulo solicitado.')
            return redirect('index')
        
        return wrapper
    return decorator
