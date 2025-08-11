from django.db import models

class Contrato(models.Model):
    nombre_entidad = models.CharField(max_length=255)
    nit_entidad = models.CharField(max_length=50)
    departamento = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    localizacion = models.CharField(max_length=255)
    orden = models.CharField(max_length=50)
    sector = models.CharField(max_length=100)
    rama = models.CharField(max_length=100)
    entidad_centralizada = models.CharField(max_length=50)
    proceso_de_compra = models.CharField(max_length=100)
    id_contrato = models.CharField(max_length=100, unique=True)
    referencia_del_contrato = models.CharField(max_length=100)
    estado_contrato = models.CharField(max_length=100)
    codigo_de_categoria_principal = models.CharField(max_length=100)
    descripcion_del_proceso = models.TextField()
    tipo_de_contrato = models.CharField(max_length=100)
    modalidad_de_contratacion = models.CharField(max_length=100)
    justificacion_modalidad = models.TextField()
    fecha_de_firma = models.DateField(null=True)
    fecha_de_inicio_del_contrato = models.DateField(null=True)
    fecha_de_fin_del_contrato = models.DateField(null=True)
    condiciones_de_entrega = models.CharField(max_length=100)
    tipodocproveedor = models.CharField(max_length=50)
    documento_proveedor = models.CharField(max_length=50)
    proveedor_adjudicado = models.CharField(max_length=255)
    es_grupo = models.CharField(max_length=50)
    es_pyme = models.CharField(max_length=50)
    habilita_pago_adelantado = models.CharField(max_length=50)
    liquidacion = models.CharField(max_length=50)
    obligacion_ambiental = models.CharField(max_length=50)
    obligaciones_postconsumo = models.CharField(max_length=50)
    reversion = models.CharField(max_length=50)
    origen_de_los_recursos = models.CharField(max_length=100)
    destino_gasto = models.CharField(max_length=100)
    valor_del_contrato = models.BigIntegerField()
    valor_de_pago_adelantado = models.BigIntegerField(default=0)
    valor_facturado = models.BigIntegerField(default=0)
    valor_pendiente_de_pago = models.BigIntegerField(default=0)
    valor_pagado = models.BigIntegerField(default=0)
    valor_amortizado = models.BigIntegerField(default=0)
    valor_pendiente_de = models.BigIntegerField(default=0)
    valor_pendiente_de_ejecucion = models.BigIntegerField(default=0)
    estado_bpin = models.CharField(max_length=100)
    codigo_bpin = models.CharField(max_length=100)
    anno_bpin = models.CharField(max_length=50)
    saldo_cdp = models.BigIntegerField(default=0)
    saldo_vigencia = models.BigIntegerField(default=0)
    es_postconflicto = models.CharField(max_length=50)
    dias_adicionados = models.IntegerField(default=0)
    puntos_del_acuerdo = models.CharField(max_length=100)
    pilares_del_acuerdo = models.CharField(max_length=100)
    url_proceso = models.URLField()
    nombre_representante_legal = models.CharField(max_length=255)
    nacionalidad_representante_legal = models.CharField(max_length=50)
    domicilio_representante_legal = models.CharField(max_length=255)
    tipo_de_identificacion_representante_legal = models.CharField(max_length=100)
    identificacion_representante_legal = models.CharField(max_length=100)
    genero_representante_legal = models.CharField(max_length=20)
    presupuesto_general_de_la_nacion_pgn = models.BigIntegerField(default=0)
    sistema_general_de_participaciones = models.BigIntegerField(default=0)
    sistema_general_de_regalias = models.BigIntegerField(default=0)
    recursos_propios_alcaldias_gobernaciones_y_resguardos_indigenas = models.BigIntegerField(default=0)
    recursos_de_credito = models.BigIntegerField(default=0)
    recursos_propios = models.BigIntegerField(default=0)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    codigo_entidad = models.CharField(max_length=100)
    codigo_proveedor = models.CharField(max_length=100)
    fecha_inicio_liquidacion = models.DateField(null=True)
    fecha_fin_liquidacion = models.DateField(null=True)
    objeto_del_contrato = models.TextField()
    duracion_del_contrato = models.CharField(max_length=100, null=True, blank=True)
    nombre_del_banco = models.CharField(max_length=100, null=True, blank=True)
    tipo_de_cuenta = models.CharField(max_length=50, null=True, blank=True)
    numero_de_cuenta = models.CharField(max_length=50, null=True, blank=True)
    el_contrato_puede_ser_prorrogado = models.BooleanField(default=False)
    nombre_ordenador_del_gasto = models.CharField(max_length=255)
    tipo_de_documento_ordenador_del_gasto = models.CharField(max_length=100)
    numero_de_documento_ordenador_del_gasto = models.CharField(max_length=100)
    nombre_supervisor = models.CharField(max_length=255)
    tipo_de_documento_supervisor = models.CharField(max_length=100)
    numero_de_documento_supervisor = models.CharField(max_length=100)
    nombre_ordenador_de_pago = models.CharField(max_length=255)
    tipo_de_documento_ordenador_de_pago = models.CharField(max_length=100)
    numero_de_documento_ordenador_de_pago = models.CharField(max_length=100)
    fecha_de_notificacion_de_prorroga = models.DateField(null=True)

    def __str__(self):
        return f"{self.id_contrato} - {self.nombre_entidad}"

class ContratoInteradministrativo(models.Model):
    """
    Modelo para almacenar datos de contratos interadministrativos de SECOP
    """
    # Información de la Entidad
    nivel_entidad = models.CharField(max_length=100, blank=True)
    codigo_entidad_en_secop = models.CharField(max_length=50, blank=True)
    nombre_de_la_entidad = models.CharField(max_length=255, blank=True)
    nit_de_la_entidad = models.CharField(max_length=50, blank=True)
    departamento_entidad = models.CharField(max_length=100, blank=True)
    municipio_entidad = models.CharField(max_length=100, blank=True)
    
    # Estado y Modalidad del Proceso
    estado_del_proceso = models.CharField(max_length=100, blank=True)
    modalidad_de_contrataci_n = models.CharField(max_length=100, blank=True)
    
    # Objeto del Contrato
    objeto_a_contratar = models.TextField(blank=True)
    objeto_del_proceso = models.TextField(blank=True)
    tipo_de_contrato = models.CharField(max_length=100, blank=True)
    
    # Fechas importantes
    fecha_de_firma_del_contrato = models.DateField(null=True, blank=True)
    fecha_inicio_ejecuci_n = models.DateField(null=True, blank=True)
    fecha_fin_ejecuci_n = models.DateField(null=True, blank=True)
    
    # Identificadores
    numero_del_contrato = models.CharField(max_length=100, blank=True)
    numero_de_proceso = models.CharField(max_length=100, unique=True)  # Clave única
    
    # Valor del contrato
    valor_contrato = models.BigIntegerField(default=0)
    
    # Información del contratista
    nom_raz_social_contratista = models.CharField(max_length=255, blank=True)
    tipo_documento_proveedor = models.CharField(max_length=50, blank=True)
    documento_proveedor = models.CharField(max_length=50, blank=True)
    
    # Información adicional
    url_contrato = models.URLField(max_length=500, blank=True)
    origen = models.CharField(max_length=50, blank=True)  # SECOP I o SECOP II
    
    # Campos de control
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Contrato Interadministrativo"
        verbose_name_plural = "Contratos Interadministrativos"
        ordering = ['-fecha_de_firma_del_contrato']
        
    def __str__(self):
        return f"{self.numero_de_proceso} - {self.nom_raz_social_contratista}"
        
    def dias_restantes(self):
        """Calcula los días restantes hasta la fecha de fin de ejecución"""
        if self.fecha_fin_ejecuci_n:
            from datetime import date
            today = date.today()
            diff = (self.fecha_fin_ejecuci_n - today).days
            return diff
        return None
        
    def get_origen_display(self):
        """Convierte el origen a un formato más legible"""
        if self.origen and 'secopii' in self.origen.lower():
            return "SECOP II"
        elif self.origen and 'secopi' in self.origen.lower():
            return "SECOP I"
        return self.origen