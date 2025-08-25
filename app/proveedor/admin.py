# app/proveedor/admin.py
from django.contrib import admin
from .models import Proveedor

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    """Admin para Proveedor siguiendo el patrón de ContratoAdmin"""
    
    list_display = [
        'nit',
        'nombre', 
        'telefono',
        'correo',
        'municipio',
        'tipo_empresa',
        'get_estado_display',
        'es_pyme_display',
        'fecha_registro'
    ]
    
    list_filter = [
        'tipo_empresa',
        'esta_activa',
        'activo',
        'espyme',
        'es_entidad',
        'es_grupo',
        'departamento',
        'fecha_registro',
        'fecha_actualizacion'
    ]
    
    search_fields = [
        'nit',
        'nombre',
        'correo',
        'telefono',
        'nombre_representante_legal',
        'n_mero_doc_representante_legal'
    ]
    
    readonly_fields = [
        'fecha_registro', 
        'fecha_actualizacion',
        'codigo'  # Si viene de la API
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'nit', 'codigo', 'tipo_empresa', 'esta_activa', 'activo')
        }),
        ('Estados del Proveedor', {
            'fields': ('es_entidad', 'es_grupo', 'espyme'),
            'classes': ('collapse',)
        }),
        ('Información de Contacto', {
            'fields': ('telefono', 'fax', 'correo', 'direccion', 'sitio_web')
        }),
        ('Ubicación', {
            'fields': ('pais', 'departamento', 'municipio', 'ubicacion')
        }),
        ('Categoría Principal', {
            'fields': ('codigo_categoria_principal', 'descripcion_categoria_principal'),
            'classes': ('collapse',)
        }),
        ('Representante Legal', {
            'fields': (
                'nombre_representante_legal',
                'tipo_doc_representante_legal', 
                'n_mero_doc_representante_legal',
                'telefono_representante_legal',
                'correo_representante_legal'
            ),
            'classes': ('collapse',)
        }),
        ('Información Adicional API', {
            'fields': (
                'camaras_comercio',
                'lista_restrictiva', 
                'inhabilidades',
                'clasificacion_organica'
            ),
            'classes': ('collapse',)
        }),
        ('Control Interno', {
            'fields': ('fecha_creacion', 'fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-fecha_registro']
    
    def get_queryset(self, request):
        """Optimizar queryset como en ContratoAdmin"""
        return super().get_queryset(request)
    
    def has_delete_permission(self, request, obj=None):
        """Permitir eliminación solo a superusuarios (como en tu patrón)"""
        return request.user.is_superuser
    
    def get_estado_display(self, obj):
        """Mostrar estado de forma legible"""
        return obj.get_estado_display()
    get_estado_display.short_description = 'Estado'
    
    def es_pyme_display(self, obj):
        """Mostrar si es PyME"""
        return "Sí" if obj.es_pyme_display() else "No"
    es_pyme_display.short_description = 'Es PyME'
    es_pyme_display.boolean = True