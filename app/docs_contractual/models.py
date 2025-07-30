# app/docs_contractual/models.py
from django.db import models

class PlantillaDocumento(models.Model):
    """Modelo para gestionar plantillas de documentos Word"""
    nombre = models.CharField(max_length=200, help_text="Nombre de la plantilla")
    descripcion = models.TextField(blank=True, help_text="Descripción de la plantilla")
    archivo_plantilla = models.FileField(upload_to='plantillas/', help_text="Archivo Word plantilla")
    activa = models.BooleanField(default=True, help_text="Si la plantilla está activa")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Plantilla de Documento"
        verbose_name_plural = "Plantillas de Documentos"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.nombre

class HistorialGeneracion(models.Model):
    """Modelo para llevar registro de documentos generados"""
    contrato_referencia = models.CharField(max_length=100, help_text="Referencia del contrato")
    plantilla_usada = models.ForeignKey(PlantillaDocumento, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=150, help_text="Usuario que generó el documento")
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    nombre_archivo_generado = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Historial de Generación"
        verbose_name_plural = "Historial de Generaciones"
        ordering = ['-fecha_generacion']
    
    def __str__(self):
        return f"{self.contrato_referencia} - {self.fecha_generacion.strftime('%Y-%m-%d %H:%M')}"