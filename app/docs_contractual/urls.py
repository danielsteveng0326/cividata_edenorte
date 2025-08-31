# app/docs_contractual/urls.py
from django.urls import path
from . import views

app_name = 'docs_contractual'

urlpatterns = [
    # Vista principal
    path('', views.docs_contractual_index, name='index'),
    
    # API para búsqueda de contratos (mantener por compatibilidad)
    path('buscar-contratos/', views.buscar_contratos, name='buscar_contratos'),
    
    # Generación de documentos (ESTA ES LA URL ORIGINAL QUE SÍ FUNCIONABA)
    path('generar-documento/', views.generar_documento, name='generar_documento'),
    
    # Historial de documentos generados
    path('historial/', views.historial_documentos, name='historial'),
    
    # Gestión de plantillas
    path('plantillas/', views.gestionar_plantillas, name='plantillas'),
    
    # Preview de variables para un contrato
    path('preview-variables/<int:contrato_id>/', views.preview_variables, name='preview_variables'),
]