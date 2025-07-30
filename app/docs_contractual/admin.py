# app/docs_contractual/admin.py
from django.contrib import admin
from .models import PlantillaDocumento, HistorialGeneracion

@admin.register(PlantillaDocumento)
class PlantillaDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa', 'fecha_creacion', 'fecha_modificacion')
    list_filter = ('activa', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'activa')
        }),
        ('Archivo', {
            'fields': ('archivo_plantilla',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )

@admin.register(HistorialGeneracion)
class HistorialGeneracionAdmin(admin.ModelAdmin):
    list_display = ('contrato_referencia', 'usuario', 'plantilla_usada', 'fecha_generacion')
    list_filter = ('fecha_generacion', 'plantilla_usada')
    search_fields = ('contrato_referencia', 'usuario', 'nombre_archivo_generado')
    readonly_fields = ('fecha_generacion',)
    
    def has_add_permission(self, request):
        # Solo lectura desde admin
        return False
    
    def has_change_permission(self, request, obj=None):
        # Solo lectura desde admin
        return False