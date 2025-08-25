# app/proveedor/models.py
from django.db import models

class Proveedor(models.Model):
    """Modelo para gestión de proveedores siguiendo la estructura de dashboard"""
    
    # Información básica del proveedor (campos principales de la API)
    nombre = models.CharField(max_length=255, verbose_name='Nombre/Razón Social')
    nit = models.CharField(max_length=50, unique=True, verbose_name='NIT')
    codigo = models.CharField(max_length=100, blank=True, verbose_name='Código')
    
    # Estados del proveedor
    es_entidad = models.CharField(max_length=10, default='false', verbose_name='Es Entidad')
    es_grupo = models.CharField(max_length=10, default='false', verbose_name='Es Grupo') 
    esta_activa = models.CharField(max_length=10, default='true', verbose_name='Está Activa')
    espyme = models.CharField(max_length=10, default='false', verbose_name='Es PyME')
    
    # Fechas (siguiendo el patrón de usar DateField)
    fecha_creacion = models.DateField(null=True, blank=True, verbose_name='Fecha de Creación')
    
    # Categoría principal
    codigo_categoria_principal = models.CharField(max_length=100, blank=True, verbose_name='Código Categoría Principal')
    descripcion_categoria_principal = models.TextField(blank=True, verbose_name='Descripción Categoría Principal')
    
    # Información de contacto
    telefono = models.CharField(max_length=50, blank=True, verbose_name='Teléfono')
    fax = models.CharField(max_length=50, blank=True, verbose_name='Fax')
    correo = models.CharField(max_length=255, blank=True, verbose_name='Correo Electrónico')
    direccion = models.CharField(max_length=500, blank=True, verbose_name='Dirección')
    sitio_web = models.CharField(max_length=500, blank=True, verbose_name='Sitio Web')
    
    # Ubicación (siguiendo tus patrones de campos)
    pais = models.CharField(max_length=100, blank=True, verbose_name='País')
    departamento = models.CharField(max_length=100, blank=True, verbose_name='Departamento')
    municipio = models.CharField(max_length=100, blank=True, verbose_name='Municipio')
    ubicacion = models.TextField(blank=True, verbose_name='Ubicación Completa')
    
    # Información empresarial
    tipo_empresa = models.CharField(max_length=100, default='PERSONA NATURAL COLOMBIANA', verbose_name='Tipo de Empresa')
    
    # Representante legal (siguiendo patrón de nombres de campos)
    nombre_representante_legal = models.CharField(max_length=255, blank=True, verbose_name='Nombre Representante Legal')
    tipo_doc_representante_legal = models.CharField(max_length=50, blank=True, verbose_name='Tipo Documento Rep. Legal')
    n_mero_doc_representante_legal = models.CharField(max_length=50, blank=True, verbose_name='Número Documento Rep. Legal')
    telefono_representante_legal = models.CharField(max_length=50, blank=True, verbose_name='Teléfono Rep. Legal')
    correo_representante_legal = models.CharField(max_length=255, blank=True, verbose_name='Correo Rep. Legal')
    
    # Campos adicionales de la API de proveedores
    camaras_comercio = models.TextField(blank=True, verbose_name='Cámaras de Comercio')
    lista_restrictiva = models.CharField(max_length=10, blank=True, verbose_name='Lista Restrictiva')
    inhabilidades = models.TextField(blank=True, verbose_name='Inhabilidades')
    clasificacion_organica = models.CharField(max_length=100, blank=True, verbose_name='Clasificación Orgánica')
    
    # Campos de control (siguiendo tu patrón)
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    activo = models.CharField(max_length=10, default='true', verbose_name='Activo en Sistema')
    
    class Meta:
        db_table = 'proveedor'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.nombre} - {self.nit}"
    
    def get_info_basica(self):
        """Retorna información básica para mostrar después de consulta (siguiendo tus patrones)"""
        info = {
            'nombre': self.nombre,
            'nit': self.nit,
            'telefono': self.telefono,
            'correo': self.correo,
            'direccion': self.direccion,
            'departamento': self.departamento,
            'municipio': self.municipio,
        }
        
        # Agregar info de representante legal si no es persona natural (como tus otros modelos)
        if self.tipo_empresa != 'PERSONA NATURAL COLOMBIANA':
            info.update({
                'nombre_representante_legal': self.nombre_representante_legal,
                'n_mero_doc_representante_legal': self.n_mero_doc_representante_legal,
                'telefono_representante_legal': self.telefono_representante_legal,
                'correo_representante_legal': self.correo_representante_legal,
            })
        
        return info
    
    def necesita_representante_legal(self):
        """Verifica si el proveedor necesita información de representante legal"""
        return self.tipo_empresa != 'PERSONA NATURAL COLOMBIANA'
    
    def get_estado_display(self):
        """Convierte el estado a formato más legible (siguiendo tu patrón)"""
        if self.esta_activa and self.esta_activa.lower() == 'true':
            return "Activo"
        return "Inactivo"
    
    def es_pyme_display(self):
        """Verifica si es PyME (siguiendo tu patrón de métodos display)"""
        return self.espyme and self.espyme.lower() == 'true'