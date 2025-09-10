# app/proveedor/models.py
from django.db import models
from datetime import date

class Proveedor(models.Model):
    """Modelo para gestión de proveedores"""
    
    # Información básica del proveedor
    nombre = models.CharField(max_length=255, verbose_name='Nombre/Razón Social')
    nit = models.CharField(max_length=50, unique=True, verbose_name='NIT')
    codigo = models.CharField(max_length=100, blank=True, verbose_name='Código')
    
    # Estados del proveedor
    es_entidad = models.CharField(max_length=10, default='false', verbose_name='Es Entidad')
    es_grupo = models.CharField(max_length=10, default='false', verbose_name='Es Grupo') 
    esta_activa = models.CharField(max_length=10, default='true', verbose_name='Está Activa')
    espyme = models.CharField(max_length=10, default='false', verbose_name='Es PyME')
    
    # Fechas
    fecha_creacion = models.DateField(null=True, blank=True, verbose_name='Fecha de Creación')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    # Categoría principal
    codigo_categoria_principal = models.CharField(max_length=100, blank=True, verbose_name='Código Categoría Principal')
    descripcion_categoria_principal = models.TextField(blank=True, verbose_name='Descripción Categoría Principal')
    
    # Información de contacto
    telefono = models.CharField(max_length=50, blank=True, verbose_name='Teléfono')
    fax = models.CharField(max_length=50, blank=True, verbose_name='Fax')
    correo = models.CharField(max_length=255, blank=True, verbose_name='Correo Electrónico')
    direccion = models.CharField(max_length=500, blank=True, verbose_name='Dirección')
    sitio_web = models.CharField(max_length=500, blank=True, verbose_name='Sitio Web')
    
    # Ubicación
    pais = models.CharField(max_length=100, blank=True, verbose_name='País')
    departamento = models.CharField(max_length=100, blank=True, verbose_name='Departamento')
    municipio = models.CharField(max_length=100, blank=True, verbose_name='Municipio')
    ubicacion = models.TextField(blank=True, verbose_name='Ubicación Completa')
    
    # Información empresarial
    tipo_empresa = models.CharField(max_length=100, default='PERSONA NATURAL COLOMBIANA', verbose_name='Tipo de Empresa')
    
    # Representante legal
    nombre_representante_legal = models.CharField(max_length=255, blank=True, verbose_name='Nombre Representante Legal')
    tipo_doc_representante_legal = models.CharField(max_length=50, blank=True, verbose_name='Tipo Documento Rep. Legal')
    n_mero_doc_representante_legal = models.CharField(max_length=50, blank=True, verbose_name='Número Documento Rep. Legal')
    telefono_representante_legal = models.CharField(max_length=50, blank=True, verbose_name='Teléfono Rep. Legal')
    correo_representante_legal = models.CharField(max_length=255, blank=True, verbose_name='Correo Rep. Legal')
    
    # Campos adicionales
    camaras_comercio = models.TextField(blank=True, verbose_name='Cámaras de Comercio')
    lista_restrictiva = models.CharField(max_length=10, blank=True, verbose_name='Lista Restrictiva')
    inhabilidades = models.TextField(blank=True, verbose_name='Inhabilidades')
    clasificacion_organica = models.CharField(max_length=100, blank=True, verbose_name='Clasificación Orgánica')
    
    # Campo activo
    activo = models.CharField(max_length=10, default='true', verbose_name='Activo en Sistema')
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        db_table = 'proveedor'
        ordering = ['-fecha_registro']
        
    def __str__(self):
        return f"{self.nombre} ({self.nit})"
    
    def save(self, *args, **kwargs):
        """Override save para validaciones"""
        # Limpiar NIT
        if self.nit:
            self.nit = self.nit.replace(' ', '').replace('-', '').replace('.', '')
        
        # Validar campos booleanos como string
        boolean_fields = ['es_entidad', 'es_grupo', 'esta_activa', 'espyme', 'activo']
        for field in boolean_fields:
            value = getattr(self, field)
            if value not in ['true', 'false']:
                setattr(self, field, 'true' if str(value).lower() in ['true', '1', 'si', 'sí'] else 'false')
        
        super().save(*args, **kwargs)
    
    @property
    def es_pyme(self):
        """Property para verificar si es PyME"""
        return self.espyme == 'true'
    
    @property
    def es_activo(self):
        """Property para verificar si está activo"""
        return self.activo == 'true'
    
    def get_info_basica(self):
        """Devolver información básica para templates"""
        return {
            'nombre': self.nombre,
            'nit': self.nit,
            'telefono': self.telefono,
            'correo': self.correo,
            'direccion': self.direccion,
            'municipio': self.municipio,
            'departamento': self.departamento,
            'tipo_empresa': self.tipo_empresa,
            'es_pyme': self.es_pyme,
            'es_activo': self.es_activo
        }
    
    def necesita_representante_legal(self):
        """Verificar si necesita representante legal"""
        return self.tipo_empresa != 'PERSONA NATURAL COLOMBIANA'