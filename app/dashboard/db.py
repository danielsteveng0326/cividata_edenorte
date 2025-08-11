from .models import Contrato, ContratoInteradministrativo  # Agregar import
from django.utils import timezone
from django.db import transaction
from datetime import datetime, date
import pytz

def process_api_data(contratos_data):
    """
    Procesa los datos de contratos recibidos de la API y los guarda en la base de datos.
    
    Args:
        contratos_data (list): Lista de diccionarios con datos de contratos
    
    Returns:
        tuple: (nuevos, actualizados, errores) - Conteo de registros procesados y errores
    """
    nuevos = 0
    actualizados = 0
    errores = 0
    
    def parse_date(date_string):
        """
        Parsea fechas y las convierte a objetos date para DateField
        """
        if not date_string:
            return None
        
        try:
            # Si la fecha viene con información de timezone (formato API)
            if 'T' in date_string and date_string.endswith('Z'):
                # Parsear fecha UTC
                dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
                # Convertir a Colombia timezone
                colombia_tz = pytz.timezone('America/Bogota')
                dt_colombia = dt.astimezone(colombia_tz)
                # IMPORTANTE: Retornar solo la fecha (sin hora) para DateField
                return dt_colombia.date()
            
            # Si es una fecha simple (YYYY-MM-DD) - formato típico de API
            elif '-' in date_string and len(date_string) >= 10:
                # Extraer solo la parte de fecha
                fecha_str = date_string[:10]  # YYYY-MM-DD
                dt = datetime.strptime(fecha_str, '%Y-%m-%d')
                return dt.date()
            
            # Si es formato DD/MM/YYYY
            elif '/' in date_string:
                dt = datetime.strptime(date_string, '%d/%m/%Y')
                return dt.date()
            
            return None
            
        except (ValueError, TypeError) as e:
            print(f"❌ Error parseando fecha {date_string}: {e}")
            return None

    def clean_number(value):
        """Convierte strings numéricos a enteros o 0 si son inválidos"""
        if not value:
            return 0
        try:
            # Limpiar caracteres especiales comunes en números
            if isinstance(value, str):
                value = value.replace(',', '').replace('$', '').replace(' ', '')
            return int(float(value))  # float primero por si hay decimales
        except (ValueError, TypeError):
            return 0

    def map_contract_data(data):
        """Mapea los datos de la API al formato del modelo"""
        return {
            'nombre_entidad': data.get('nombre_entidad', ''),
            'nit_entidad': data.get('nit_entidad', ''),
            'departamento': data.get('departamento', ''),
            'ciudad': data.get('ciudad', ''),
            'localizacion': data.get('localizaci_n', ''),
            'orden': data.get('orden', ''),
            'sector': data.get('sector', ''),
            'rama': data.get('rama', ''),
            'entidad_centralizada': data.get('entidad_centralizada', ''),
            'proceso_de_compra': data.get('proceso_de_compra', ''),
            'id_contrato': data.get('id_contrato', ''),
            'referencia_del_contrato': data.get('referencia_del_contrato', ''),
            'estado_contrato': data.get('estado_contrato', ''),
            'codigo_de_categoria_principal': data.get('codigo_de_categoria_principal', ''),
            'descripcion_del_proceso': data.get('descripcion_del_proceso', ''),
            'tipo_de_contrato': data.get('tipo_de_contrato', ''),
            'modalidad_de_contratacion': data.get('modalidad_de_contratacion', ''),
            'justificacion_modalidad': data.get('justificacion_modalidad_de', ''),
            
            # FECHAS - Ahora usando parse_date que retorna objetos date
            'fecha_de_firma': parse_date(data.get('fecha_de_firma')),
            'fecha_de_inicio_del_contrato': parse_date(data.get('fecha_de_inicio_del_contrato')),
            'fecha_de_fin_del_contrato': parse_date(data.get('fecha_de_fin_del_contrato')),
            'fecha_inicio_liquidacion': parse_date(data.get('fecha_inicio_liquidacion')),
            'fecha_fin_liquidacion': parse_date(data.get('fecha_fin_liquidacion')),
            'fecha_de_notificacion_de_prorroga': parse_date(data.get('fecha_de_notificacion_de_prorroga')),
            
            'condiciones_de_entrega': data.get('condiciones_de_entrega', ''),
            'tipodocproveedor': data.get('tipodocproveedor', ''),
            'documento_proveedor': data.get('documento_proveedor', ''),
            'proveedor_adjudicado': data.get('proveedor_adjudicado', ''),
            'es_grupo': data.get('es_grupo', ''),
            'es_pyme': data.get('es_pyme', ''),
            'habilita_pago_adelantado': data.get('habilita_pago_adelantado', ''),
            'liquidacion': data.get('liquidaci_n', ''),
            'obligacion_ambiental': data.get('obligaci_n_ambiental', ''),
            'obligaciones_postconsumo': data.get('obligaciones_postconsumo', ''),
            'reversion': data.get('reversion', ''),
            'origen_de_los_recursos': data.get('origen_de_los_recursos', ''),
            'destino_gasto': data.get('destino_gasto', ''),
            
            # VALORES NUMÉRICOS
            'valor_del_contrato': clean_number(data.get('valor_del_contrato')),
            'valor_de_pago_adelantado': clean_number(data.get('valor_de_pago_adelantado')),
            'valor_facturado': clean_number(data.get('valor_facturado')),
            'valor_pendiente_de_pago': clean_number(data.get('valor_pendiente_de_pago')),
            'valor_pagado': clean_number(data.get('valor_pagado')),
            'valor_amortizado': clean_number(data.get('valor_amortizado')),
            'valor_pendiente_de': clean_number(data.get('valor_pendiente_de')),
            'valor_pendiente_de_ejecucion': clean_number(data.get('valor_pendiente_de_ejecucion')),
            'saldo_cdp': clean_number(data.get('saldo_cdp')),
            'saldo_vigencia': clean_number(data.get('saldo_vigencia')),
            'dias_adicionados': clean_number(data.get('dias_adicionados')),
            
            'estado_bpin': data.get('estado_bpin', ''),
            'codigo_bpin': data.get('c_digo_bpin', ''),
            'anno_bpin': data.get('anno_bpin', ''),
            'es_postconflicto': data.get('espostconflicto', ''),
            'puntos_del_acuerdo': data.get('puntos_del_acuerdo', ''),
            'pilares_del_acuerdo': data.get('pilares_del_acuerdo', ''),
            'url_proceso': data.get('urlproceso', {}).get('url', '') if isinstance(data.get('urlproceso'), dict) else data.get('urlproceso', ''),
            
            # REPRESENTANTE LEGAL
            'nombre_representante_legal': data.get('nombre_representante_legal', ''),
            'nacionalidad_representante_legal': data.get('nacionalidad_representante_legal', ''),
            'domicilio_representante_legal': data.get('domicilio_representante_legal', ''),
            'tipo_de_identificacion_representante_legal': data.get('tipo_de_identificaci_n_representante_legal', ''),
            'identificacion_representante_legal': data.get('identificaci_n_representante_legal', ''),
            'genero_representante_legal': data.get('g_nero_representante_legal', ''),
            
            # PRESUPUESTO
            'presupuesto_general_de_la_nacion_pgn': clean_number(data.get('presupuesto_general_de_la_nacion_pgn')),
            'sistema_general_de_participaciones': clean_number(data.get('sistema_general_de_participaciones')),
            'sistema_general_de_regalias': clean_number(data.get('sistema_general_de_regal_as')),
            'recursos_propios_alcaldias_gobernaciones_y_resguardos_indigenas': clean_number(data.get('recursos_propios_alcald_as_gobernaciones_y_resguardos_ind_genas_')),
            'recursos_de_credito': clean_number(data.get('recursos_de_credito')),
            'recursos_propios': clean_number(data.get('recursos_propios')),
            
            'codigo_entidad': data.get('codigo_entidad', ''),
            'codigo_proveedor': data.get('codigo_proveedor', ''),
            'objeto_del_contrato': data.get('objeto_del_contrato', ''),
            'duracion_del_contrato': data.get('duraci_n_del_contrato', ''),
            'nombre_del_banco': data.get('nombre_del_banco', ''),
            'tipo_de_cuenta': data.get('tipo_de_cuenta', ''),
            'numero_de_cuenta': data.get('n_mero_de_cuenta', ''),
            'el_contrato_puede_ser_prorrogado': data.get('el_contrato_puede_ser_prorrogado', '') == 'Si',
            
            # FUNCIONARIOS
            'nombre_ordenador_del_gasto': data.get('nombre_ordenador_del_gasto', ''),
            'tipo_de_documento_ordenador_del_gasto': data.get('tipo_de_documento_ordenador_del_gasto', ''),
            'numero_de_documento_ordenador_del_gasto': data.get('n_mero_de_documento_ordenador_del_gasto', ''),
            'nombre_supervisor': data.get('nombre_supervisor', ''),
            'tipo_de_documento_supervisor': data.get('tipo_de_documento_supervisor', ''),
            'numero_de_documento_supervisor': data.get('n_mero_de_documento_supervisor', ''),
            'nombre_ordenador_de_pago': data.get('nombre_ordenador_de_pago', ''),
            'tipo_de_documento_ordenador_de_pago': data.get('tipo_de_documento_ordenador_de_pago', ''),
            'numero_de_documento_ordenador_de_pago': data.get('n_mero_de_documento_ordenador_de_pago', ''),
            
            # ultima_actualizacion se actualiza automáticamente con auto_now=True
        }

    # Procesamos cada contrato
    for contrato_data in contratos_data:
        try:
            with transaction.atomic():
                # Mapeamos los datos
                cleaned_data = map_contract_data(contrato_data)
                
                # Logging para debugging
                print(f"🔄 Procesando contrato: {cleaned_data.get('id_contrato')}")
                print(f"   - Fecha firma: {cleaned_data.get('fecha_de_firma')} (tipo: {type(cleaned_data.get('fecha_de_firma'))})")
                print(f"   - Fecha fin: {cleaned_data.get('fecha_de_fin_del_contrato')} (tipo: {type(cleaned_data.get('fecha_de_fin_del_contrato'))})")
                
                # Verificamos si el contrato existe
                contrato, created = Contrato.objects.update_or_create(
                    id_contrato=cleaned_data['id_contrato'],
                    defaults=cleaned_data
                )
                
                if created:
                    nuevos += 1
                    print(f"✅ Nuevo contrato creado: {cleaned_data['id_contrato']}")
                else:
                    actualizados += 1
                    print(f"🔄 Contrato actualizado: {cleaned_data['id_contrato']}")
                    
        except Exception as e:
            print(f"❌ Error procesando contrato {contrato_data.get('id_contrato')}: {str(e)}")
            errores += 1
            continue

    print(f"📊 Resumen de procesamiento: {nuevos} nuevos, {actualizados} actualizados, {errores} errores")
    return nuevos, actualizados, errores


def process_interadmin_api_data(contratos_data):
    """
    Procesa los datos de contratos interadministrativos recibidos de la API y los guarda en la base de datos.
    
    Args:
        contratos_data (list): Lista de diccionarios con datos de contratos interadministrativos
    
    Returns:
        tuple: (nuevos, actualizados, errores) - Conteo de registros procesados y errores
    """
    nuevos = 0
    actualizados = 0
    errores = 0
    
    def parse_date(date_string):
        """
        Parsea fechas y las convierte a objetos date para DateField
        """
        if not date_string:
            return None
        
        try:
            # Si la fecha viene con información de timezone (formato API)
            if 'T' in date_string and date_string.endswith('Z'):
                # Parsear fecha UTC
                dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
                # Convertir a Colombia timezone
                colombia_tz = pytz.timezone('America/Bogota')
                dt_colombia = dt.astimezone(colombia_tz)
                # IMPORTANTE: Retornar solo la fecha (sin hora) para DateField
                return dt_colombia.date()
            
            # Si es una fecha simple (YYYY-MM-DD) - formato típico de API
            elif '-' in date_string and len(date_string) >= 10:
                # Extraer solo la parte de fecha
                fecha_str = date_string[:10]  # YYYY-MM-DD
                dt = datetime.strptime(fecha_str, '%Y-%m-%d')
                return dt.date()
            
            # Si es formato DD/MM/YYYY
            elif '/' in date_string:
                dt = datetime.strptime(date_string, '%d/%m/%Y')
                return dt.date()
            
            return None
            
        except (ValueError, TypeError) as e:
            print(f"❌ Error parseando fecha {date_string}: {e}")
            return None

    def clean_number(value):
        """Convierte strings numéricos a enteros o 0 si son inválidos"""
        if not value:
            return 0
        try:
            # Limpiar caracteres especiales comunes en números
            if isinstance(value, str):
                value = value.replace(',', '').replace('$', '').replace(' ', '')
            return int(float(value))  # float primero por si hay decimales
        except (ValueError, TypeError):
            return 0

    def map_interadmin_data(data):
        """Mapea los datos de la API al formato del modelo ContratoInteradministrativo"""
        return {
            'nivel_entidad': data.get('nivel_entidad', ''),
            'codigo_entidad_en_secop': data.get('codigo_entidad_en_secop', ''),
            'nombre_de_la_entidad': data.get('nombre_de_la_entidad', ''),
            'nit_de_la_entidad': data.get('nit_de_la_entidad', ''),
            'departamento_entidad': data.get('departamento_entidad', ''),
            'municipio_entidad': data.get('municipio_entidad', ''),
            
            'estado_del_proceso': data.get('estado_del_proceso', ''),
            'modalidad_de_contrataci_n': data.get('modalidad_de_contrataci_n', ''),
            
            'objeto_a_contratar': data.get('objeto_a_contratar', ''),
            'objeto_del_proceso': data.get('objeto_del_proceso', ''),
            'tipo_de_contrato': data.get('tipo_de_contrato', ''),
            
            # FECHAS
            'fecha_de_firma_del_contrato': parse_date(data.get('fecha_de_firma_del_contrato')),
            'fecha_inicio_ejecuci_n': parse_date(data.get('fecha_inicio_ejecuci_n')),
            'fecha_fin_ejecuci_n': parse_date(data.get('fecha_fin_ejecuci_n')),
            
            'numero_del_contrato': data.get('numero_del_contrato', ''),
            'numero_de_proceso': data.get('numero_de_proceso', ''),
            
            'valor_contrato': clean_number(data.get('valor_contrato')),
            
            'nom_raz_social_contratista': data.get('nom_raz_social_contratista', ''),
            'tipo_documento_proveedor': data.get('tipo_documento_proveedor', ''),
            'documento_proveedor': data.get('documento_proveedor', ''),
            
            'url_contrato': data.get('url_contrato', ''),
            'origen': data.get('origen', ''),
        }

    # Procesar cada contrato de la lista
    for contrato_data in contratos_data:
        try:
            with transaction.atomic():
                numero_proceso = contrato_data.get('numero_de_proceso')
                
                if not numero_proceso:
                    print(f"⚠️ Saltando registro sin número de proceso")
                    errores += 1
                    continue
                
                # Buscar si ya existe el contrato
                contrato_existente = ContratoInteradministrativo.objects.filter(
                    numero_de_proceso=numero_proceso
                ).first()
                
                # Mapear los datos
                datos_mapeados = map_interadmin_data(contrato_data)
                
                if contrato_existente:
                    # Actualizar registro existente
                    for campo, valor in datos_mapeados.items():
                        setattr(contrato_existente, campo, valor)
                    
                    contrato_existente.save()
                    actualizados += 1
                    print(f"✅ Actualizado: {numero_proceso}")
                    
                else:
                    # Crear nuevo registro
                    nuevo_contrato = ContratoInteradministrativo(**datos_mapeados)
                    nuevo_contrato.save()
                    nuevos += 1
                    print(f"🆕 Nuevo: {numero_proceso}")
                    
        except Exception as e:
            print(f"❌ Error procesando contrato {contrato_data.get('numero_de_proceso', 'SIN_ID')}: {str(e)}")
            errores += 1
            continue
    
    print(f"📊 Procesamiento completado - Nuevos: {nuevos}, Actualizados: {actualizados}, Errores: {errores}")
    return (nuevos, actualizados, errores)