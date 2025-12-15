from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Modulo(models.Model):
    """
    Modelo para definir los módulos del sistema.
    Cada módulo representa una sección de la aplicación.
    """
    MODULOS_CHOICES = [
        ('contratacion', 'Contratación'),
        ('asistente_contratacion', 'Asistente Contratación'),
        ('proveedores', 'Proveedores'),
        ('paa', 'PAA'),
        ('docs_contractual', 'Documentos Contractuales'),
        ('chatbot', 'Chatbot Emil-IA'),
        ('reportes', 'Reportes'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True, choices=MODULOS_CHOICES)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    icono = models.CharField(max_length=50, default='fas fa-folder')
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        return self.nombre


class PerfilUsuario(models.Model):
    """
    Extensión del modelo User de Django para agregar campos personalizados.
    Incluye gestión de permisos por módulos y contraseña temporal.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    # Identificación
    numero_id = models.CharField(max_length=20, unique=True, verbose_name='Número de Identificación')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    
    # Permisos por módulos
    modulos_permitidos = models.ManyToManyField(Modulo, blank=True, related_name='usuarios')
    
    # Control de contraseña temporal
    password_temporal = models.BooleanField(default=True, verbose_name='Contraseña Temporal')
    fecha_cambio_password = models.DateTimeField(null=True, blank=True)
    
    # Configuración de usuario
    es_superusuario_sistema = models.BooleanField(default=False, verbose_name='Super Usuario del Sistema')
    puede_gestionar_usuarios = models.BooleanField(default=False, verbose_name='Puede Gestionar Usuarios')
    
    # Auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios_creados')
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.numero_id}"
    
    def tiene_acceso_modulo(self, codigo_modulo):
        """Verifica si el usuario tiene acceso a un módulo específico"""
        if self.es_superusuario_sistema or self.user.is_superuser:
            return True
        return self.modulos_permitidos.filter(codigo=codigo_modulo, activo=True).exists()
    
    def requiere_cambio_password(self):
        """Verifica si el usuario debe cambiar su contraseña"""
        return self.password_temporal


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crea automáticamente un perfil cuando se crea un usuario"""
    if created:
        PerfilUsuario.objects.create(user=instance)


@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    """Guarda el perfil cuando se guarda el usuario"""
    if hasattr(instance, 'perfil'):
        instance.perfil.save()
