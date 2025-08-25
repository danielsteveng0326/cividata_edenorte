# app/proveedor/urls.py
from django.urls import path
from . import views
from .views import ProveedorListView

app_name = 'proveedor'

urlpatterns = [
    # Vista principal (siguiendo el patrón de dashboard)
    path('', views.index, name="index"),
    
    # Consulta de proveedores por NIT (AJAX)
    path('consultar-nit/', views.consultar_nit, name='consultar_nit'),
    
    # Detalle y edición
    path('detalle/<int:proveedor_id>/', views.detalle_proveedor, name='detalle'),
    
    # Registro manual
    path('registrar/', views.registrar_proveedor, name='registrar'),
    
    # Listado simple
    path('listar/', views.listar_proveedores, name='listar'),
    
    # API para sincronización masiva (siguiendo el patrón de dashboard/api)
    path('api/', views.api_proveedores, name="api"),
    
    # Vista de tabla con ListView (siguiendo el patrón de ContratoListView)
    path('tabla/', ProveedorListView.as_view(), name='tabla_proveedores'),
]