# app/proveedor/apps.py
from django.apps import AppConfig

class ProveedorConfig(AppConfig):
    """Configuración de la app proveedor siguiendo el patrón del proyecto"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'proveedor'
    verbose_name = 'Gestión de Proveedores'