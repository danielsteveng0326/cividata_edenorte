# app/proveedor/urls.py
from django.urls import path
from . import views
from .views import ProveedorListView

app_name = 'proveedor'

urlpatterns = [
    # Vista principal
    path('', views.index, name="index"),
    
    # Consulta de proveedores por NIT (AJAX)
    path('consultar-nit/', views.consultar_nit, name='consultar_nit'),
    
    # Detalle y edición
    path('detalle/<int:proveedor_id>/', views.detalle_proveedor, name='detalle'),
    
    # Registro manual
    path('registrar/', views.registrar_proveedor, name='registrar'),
    
    # Listado simple
    path('listar/', views.listar_proveedores, name='listar'),
    
    # API para sincronización masiva - SOLO ACCESIBLE POR URL
    path('api/sincronizar/', views.api_proveedores, name="api"),
    
    # Vista de tabla con ListView
    path('tabla/', ProveedorListView.as_view(), name='tabla_proveedores'),
]