from .models import Modulo


def permisos_usuario(request):
    """
    Context processor que agrega información de permisos del usuario
    a todos los templates.
    """
    context = {
        'puede_gestionar_usuarios': False,
        'es_superusuario_sistema': False,
        'modulos_usuario': [],
    }
    
    if request.user.is_authenticated and hasattr(request.user, 'perfil'):
        perfil = request.user.perfil
        
        context['puede_gestionar_usuarios'] = (
            perfil.puede_gestionar_usuarios or 
            perfil.es_superusuario_sistema or 
            request.user.is_superuser
        )
        context['es_superusuario_sistema'] = (
            perfil.es_superusuario_sistema or 
            request.user.is_superuser
        )
        
        # Si es superusuario, tiene acceso a todos los módulos
        if context['es_superusuario_sistema']:
            context['modulos_usuario'] = Modulo.objects.filter(activo=True)
        else:
            context['modulos_usuario'] = perfil.modulos_permitidos.filter(activo=True)
    
    return context
