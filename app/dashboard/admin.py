# dashboard/admin.py - Agregar al archivo existente

from django.contrib import admin
from .models import Contrato, ContratoInteradministrativo

# Registrar el modelo existente Contrato (si no está ya registrado)
@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ['id_contrato', 'proveedor_adjudicado', 'fecha_de_firma', 'valor_del_contrato']
    list_filter = ['fecha_de_firma', 'modalidad_de_contratacion', 'estado_contrato']
    search_fields = ['id_contrato', 'proveedor_adjudicado', 'descripcion_del_proceso']
    ordering = ['-fecha_de_firma']

# Nuevo registro para ContratoInteradministrativo
@admin.register(ContratoInteradministrativo)
class ContratoInteradministrativoAdmin(admin.ModelAdmin):
    list_display = [
        'numero_de_proceso', 
        'nom_raz_social_contratista', 
        'municipio_entidad',
        'fecha_de_firma_del_contrato', 
        'fecha_fin_ejecuci_n',
        'valor_contrato',
        'estado_del_proceso'
    ]
    
    list_filter = [
        'fecha_de_firma_del_contrato',
        'municipio_entidad',
        'departamento_entidad',
        'estado_del_proceso',
        'tipo_de_contrato',
        'origen'
    ]
    
    search_fields = [
        'numero_de_proceso',
        'numero_del_contrato',
        'nom_raz_social_contratista',
        'documento_proveedor',
        'objeto_a_contratar'
    ]
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información del Proceso', {
            'fields': ('numero_de_proceso', 'numero_del_contrato', 'estado_del_proceso')
        }),
        ('Entidad Contratante', {
            'fields': ('nombre_de_la_entidad', 'nit_de_la_entidad', 'municipio_entidad', 'departamento_entidad')
        }),
        ('Contratista', {
            'fields': ('nom_raz_social_contratista', 'tipo_documento_proveedor', 'documento_proveedor')
        }),
        ('Detalles del Contrato', {
            'fields': ('tipo_de_contrato', 'modalidad_de_contrataci_n', 'objeto_a_contratar', 'valor_contrato')
        }),
        ('Fechas', {
            'fields': ('fecha_de_firma_del_contrato', 'fecha_inicio_ejecuci_n', 'fecha_fin_ejecuci_n')
        }),
        ('Información Adicional', {
            'fields': ('url_contrato', 'origen', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-fecha_de_firma_del_contrato']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()