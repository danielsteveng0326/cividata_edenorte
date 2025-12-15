# app/login/urls.py
from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('check-auth/', views.check_auth_status, name='check_auth'),
    
    # Gestión de usuarios
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:user_id>/', views.detalle_usuario, name='detalle_usuario'),
    path('usuarios/<int:user_id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:user_id>/resetear-password/', views.resetear_password, name='resetear_password'),
    path('usuarios/<int:user_id>/toggle-activo/', views.toggle_usuario_activo, name='toggle_usuario_activo'),
    
    # Cambio de contraseña
    path('primer-cambio-password/', views.primer_cambio_password, name='primer_cambio_password'),
    path('cambiar-password/', views.cambiar_mi_password, name='cambiar_password'),
]