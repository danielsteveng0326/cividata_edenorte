# app/login/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from .models import PerfilUsuario, Modulo
from .forms import (
    CrearUsuarioForm, EditarUsuarioForm, CambiarPasswordForm,
    PrimerCambioPasswordForm, ResetearPasswordForm
)
from .decorators import superuser_required, puede_gestionar_usuarios_required

@never_cache
@csrf_protect
def login_view(request):
    """Vista de login con diseño AdminLTE"""
    
    # Si el usuario ya está autenticado, redirigir directamente al index de contratación
    if request.user.is_authenticated:
        return redirect('/contratacion/index/')  
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.get_full_name() or user.username}!')
                
                # Redirigir a la página solicitada o al dashboard
                next_url = request.GET.get('next', '/contratacion/index/')
                return HttpResponseRedirect(next_url)
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Por favor complete todos los campos')
    
    return render(request, 'login/login.html')

@login_required
def logout_view(request):
    """Vista de logout"""
    user_name = request.user.get_full_name() or request.user.username
    logout(request)
    messages.info(request, f'Sesión cerrada correctamente. ¡Hasta pronto {user_name}!')
    return redirect('login:login')

def check_auth_status(request):
    """Vista para verificar estado de autenticación via AJAX"""
    return JsonResponse({
        'authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None
    })

@login_required
def primer_cambio_password(request):
    """Vista para el primer cambio de contraseña obligatorio"""
    if not hasattr(request.user, 'perfil') or not request.user.perfil.requiere_cambio_password():
        return redirect('index')
    
    if request.method == 'POST':
        form = PrimerCambioPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, '¡Contraseña actualizada exitosamente! Ya puedes usar el sistema.')
            return redirect('index')
    else:
        form = PrimerCambioPasswordForm(request.user)
    
    return render(request, 'login/primer_cambio_password.html', {'form': form})

@login_required
@puede_gestionar_usuarios_required
def lista_usuarios(request):
    """Vista para listar todos los usuarios del sistema"""
    query = request.GET.get('q', '')
    
    usuarios = User.objects.select_related('perfil').all()
    
    if query:
        usuarios = usuarios.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(perfil__numero_id__icontains=query)
        )
    
    usuarios = usuarios.order_by('-date_joined')
    
    context = {
        'usuarios': usuarios,
        'query': query,
    }
    return render(request, 'login/lista_usuarios.html', context)

@login_required
@puede_gestionar_usuarios_required
def crear_usuario(request):
    """Vista para crear un nuevo usuario"""
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(creado_por=request.user)
            
            password_temporal = form.password_temporal
            
            email_enviado = False
            try:
                enviar_email_bienvenida(user, password_temporal)
                email_enviado = True
                messages.success(
                    request,
                    f'Usuario {user.get_full_name()} creado exitosamente. '
                    f'Se ha enviado un correo electrónico con la contraseña temporal.'
                )
            except Exception as e:
                messages.warning(
                    request,
                    f'Usuario creado exitosamente, pero no se pudo enviar el correo electrónico. '
                    f'Por favor, copia la contraseña temporal que se muestra abajo y envíala manualmente al usuario.'
                )
            
            # Redirigir a página de confirmación con la contraseña
            context = {
                'usuario': user,
                'password_temporal': password_temporal,
                'email_enviado': email_enviado,
                'es_nuevo': True,
            }
            return render(request, 'login/usuario_creado_confirmacion.html', context)
    else:
        form = CrearUsuarioForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Nuevo Usuario',
    }
    return render(request, 'login/crear_usuario.html', context)

@login_required
@puede_gestionar_usuarios_required
def editar_usuario(request, user_id):
    """Vista para editar un usuario existente"""
    usuario = get_object_or_404(User, id=user_id)
    perfil = usuario.perfil
    
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario, perfil=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario {usuario.get_full_name()} actualizado exitosamente.')
            return redirect('login:lista_usuarios')
    else:
        form = EditarUsuarioForm(instance=usuario, perfil=perfil)
    
    context = {
        'form': form,
        'usuario': usuario,
        'titulo': f'Editar Usuario: {usuario.get_full_name()}',
    }
    return render(request, 'login/editar_usuario.html', context)

@login_required
@puede_gestionar_usuarios_required
def detalle_usuario(request, user_id):
    """Vista para ver detalles de un usuario"""
    usuario = get_object_or_404(User, id=user_id)
    perfil = usuario.perfil
    
    context = {
        'usuario': usuario,
        'perfil': perfil,
    }
    return render(request, 'login/detalle_usuario.html', context)

@login_required
@puede_gestionar_usuarios_required
def resetear_password(request, user_id):
    """Vista para resetear la contraseña de un usuario"""
    usuario = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = ResetearPasswordForm(usuario, request.POST)
        if form.is_valid():
            form.save()
            password_temporal = form.password_temporal
            
            email_enviado = False
            try:
                enviar_email_reset_password(usuario, password_temporal)
                email_enviado = True
                messages.success(
                    request,
                    f'Contraseña reseteada para {usuario.get_full_name()}. '
                    f'Se ha enviado un correo electrónico con la nueva contraseña temporal.'
                )
            except Exception as e:
                messages.warning(
                    request,
                    f'Contraseña reseteada exitosamente, pero no se pudo enviar el correo electrónico. '
                    f'Por favor, copia la contraseña temporal que se muestra abajo y envíala manualmente al usuario.'
                )
            
            # Redirigir a una página de confirmación con la contraseña
            context = {
                'usuario': usuario,
                'password_temporal': password_temporal,
                'email_enviado': email_enviado,
            }
            return render(request, 'login/password_reseteado_confirmacion.html', context)
    else:
        form = ResetearPasswordForm(usuario)
    
    context = {
        'form': form,
        'usuario': usuario,
    }
    return render(request, 'login/resetear_password.html', context)

@login_required
def cambiar_mi_password(request):
    """Vista para que el usuario cambie su propia contraseña"""
    if request.method == 'POST':
        form = CambiarPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            
            if hasattr(user, 'perfil'):
                user.perfil.password_temporal = False
                user.perfil.fecha_cambio_password = timezone.now()
                user.perfil.save()
            
            messages.success(request, '¡Tu contraseña ha sido actualizada exitosamente!')
            return redirect('index')
    else:
        form = CambiarPasswordForm(request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'login/cambiar_password.html', context)

@login_required
@puede_gestionar_usuarios_required
def toggle_usuario_activo(request, user_id):
    """Vista para activar/desactivar un usuario"""
    if request.method == 'POST':
        usuario = get_object_or_404(User, id=user_id)
        
        if usuario.perfil.es_superusuario_sistema:
            return JsonResponse({
                'success': False,
                'message': 'No se puede desactivar un superusuario del sistema'
            })
        
        usuario.perfil.activo = not usuario.perfil.activo
        usuario.perfil.save()
        usuario.is_active = usuario.perfil.activo
        usuario.save()
        
        estado = 'activado' if usuario.perfil.activo else 'desactivado'
        
        return JsonResponse({
            'success': True,
            'activo': usuario.perfil.activo,
            'message': f'Usuario {estado} exitosamente'
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

def enviar_email_bienvenida(user, password_temporal):
    """Envía email de bienvenida con contraseña temporal"""
    asunto = 'Bienvenido a CiviData - Edenorte'
    mensaje = f"""
    Hola {user.get_full_name()},
    
    Tu cuenta ha sido creada exitosamente en el sistema CiviData - Edenorte.
    
    Tus credenciales de acceso son:
    Usuario: {user.username}
    Contraseña temporal: {password_temporal}
    
    Por seguridad, deberás cambiar tu contraseña en el primer inicio de sesión.
    
    Puedes acceder al sistema en: {settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'}
    
    Si tienes alguna pregunta, no dudes en contactar al administrador del sistema.
    
    Saludos,
    Equipo CiviData
    """
    
    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def enviar_email_reset_password(user, password_temporal):
    """Envía email con nueva contraseña temporal"""
    asunto = 'Contraseña Reseteada - CiviData Edenorte'
    mensaje = f"""
    Hola {user.get_full_name()},
    
    Tu contraseña ha sido reseteada por un administrador del sistema.
    
    Tu nueva contraseña temporal es: {password_temporal}
    
    Por seguridad, deberás cambiar esta contraseña en tu próximo inicio de sesión.
    
    Si no solicitaste este cambio, contacta inmediatamente al administrador del sistema.
    
    Saludos,
    Equipo CiviData
    """
    
    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )