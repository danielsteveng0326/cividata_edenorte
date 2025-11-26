# app/proveedor/admin.py
from django.contrib import admin
from .models import Proveedor

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    """Admin para Proveedor"""
    
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
        'fecha_creacion',
        'fecha_registro', 
        'fecha_actualizacion',
        'codigo'
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
        ('Información Adicional', {
            'fields': (
                'camaras_comercio',
                'lista_restrictiva', 
                'inhabilidades',
                'clasificacion_organica'
            ),
            'classes': ('collapse',)
        }),
        ('Fechas y Control', {
            'fields': ('fecha_creacion', 'fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-fecha_registro']
    
    def get_queryset(self, request):
        """Optimizar queryset"""
        return super().get_queryset(request)
    
    def has_delete_permission(self, request, obj=None):
        """Permitir eliminación solo a superusuarios"""
        return request.user.is_superuser
    
    def get_estado_display(self, obj):
        """Mostrar estado de forma legible"""
        if obj.activo == 'true':
            return "Activo "
        else:
            return "Inactivo "
    get_estado_display.short_description = 'Estado'
    
    def es_pyme_display(self, obj):
        """Mostrar si es PyME"""
        return obj.espyme == 'true'
    es_pyme_display.short_description = 'Es PyME'
    es_pyme_display.boolean = True
    
    def save_model(self, request, obj, form, change):
        """Override save_model para logs"""
        action = "Actualizado" if change else "Creado"
        super().save_model(request, obj, form, change)
        self.message_user(request, f'Proveedor {obj.nit} {action.lower()} exitosamente.')
    
    # Acciones personalizadas
    actions = ['activar_proveedores', 'desactivar_proveedores']
    
    def activar_proveedores(self, request, queryset):
        """Acción para activar proveedores seleccionados"""
        updated = queryset.update(activo='true')
        self.message_user(request, f'{updated} proveedores activados.')
    activar_proveedores.short_description = "Activar proveedores seleccionados"
    
    def desactivar_proveedores(self, request, queryset):
        """Acción para desactivar proveedores seleccionados"""
        updated = queryset.update(activo='false')
        self.message_user(request, f'{updated} proveedores desactivados.')
    desactivar_proveedores.short_description = "Desactivar proveedores seleccionados"