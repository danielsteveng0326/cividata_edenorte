# app/proveedor/db.py
import json
from datetime import datetime
from django.db import transaction
from .models import Proveedor
from .utils import limpiar_datos_proveedor

def get_proveedores_stats():
    """Obtener estadísticas básicas de proveedores"""
    try:
        total = Proveedor.objects.count()
        activos = Proveedor.objects.filter(activo='true').count()
        inactivos = total - activos
        pymes = Proveedor.objects.filter(espyme='true').count()
        personas_naturales = Proveedor.objects.filter(tipo_empresa='PERSONA NATURAL COLOMBIANA').count()
        empresas = total - personas_naturales
        
        return {
            'total': total,
            'activos': activos,
            'inactivos': inactivos,
            'pymes': pymes,
            'personas_naturales': personas_naturales,
            'empresas': empresas
        }
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {str(e)}")
        return {
            'total': 0,
            'activos': 0,
            'inactivos': 0,
            'pymes': 0,
            'personas_naturales': 0,
            'empresas': 0
        }

def parse_date(date_string):
    """Parsea fechas desde strings de la API"""
    if not date_string:
        return None
    
    try:
        # Intentar diferentes formatos de fecha
        formats = ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f']
        
        for fmt in formats:
            try:
                parsed_date = datetime.strptime(date_string, fmt)
                return parsed_date.date()
            except ValueError:
                continue
        
        print(f"⚠️ No se pudo parsear la fecha: {date_string}")
        return None
        
    except Exception as e:
        print(f"❌ Error parseando fecha {date_string}: {str(e)}")
        return None

def map_proveedor_data(data):
    """Mapea los datos de la API al formato del modelo Proveedor"""
    try:
        return {
            'nombre': data.get('nombre', ''),
            'nit': data.get('nit', ''),
            'codigo': data.get('codigo', ''),
            'es_entidad': data.get('es_entidad', 'false'),
            'es_grupo': data.get('es_grupo', 'false'),
            'esta_activa': data.get('esta_activa', 'true'),
            'espyme': data.get('espyme', 'false'),
            
            # Fechas usando parse_date
            'fecha_creacion': parse_date(data.get('fecha_creacion')),
            
            # Categoría principal
            'codigo_categoria_principal': data.get('codigo_categoria_principal', ''),
            'descripcion_categoria_principal': data.get('descripcion_categoria_principal', ''),
            
            # Información de contacto
            'telefono': data.get('telefono', ''),
            'fax': data.get('fax', ''),
            'correo': data.get('correo', ''),
            'direccion': data.get('direccion', ''),
            'sitio_web': data.get('sitio_web', ''),
            
            # Ubicación
            'pais': data.get('pais', ''),
            'departamento': data.get('departamento', ''),
            'municipio': data.get('municipio', ''),
            'ubicacion': data.get('ubicacion', ''),
            
            # Información empresarial
            'tipo_empresa': data.get('tipo_empresa', 'PERSONA NATURAL COLOMBIANA'),
            
            # Representante legal
            'nombre_representante_legal': data.get('nombre_representante_legal', ''),
            'tipo_doc_representante_legal': data.get('tipo_doc_representante_legal', ''),
            'n_mero_doc_representante_legal': data.get('n_mero_doc_representante_legal', ''),
            'telefono_representante_legal': data.get('telefono_representante_legal', ''),
            'correo_representante_legal': data.get('correo_representante_legal', ''),
            
            # Campos adicionales
            'camaras_comercio': data.get('camaras_comercio', ''),
            'lista_restrictiva': data.get('lista_restrictiva', ''),
            'inhabilidades': data.get('inhabilidades', ''),
            'clasificacion_organica': data.get('clasificacion_organica', ''),
            
            # Campo activo (por defecto true)
            'activo': 'true'
        }
    except Exception as e:
        print(f"❌ Error mapeando datos de proveedor: {str(e)}")
        return {}

def process_single_proveedor_data(proveedor_data):
    """Procesa un solo proveedor desde la API y lo guarda/actualiza en la base de datos"""
    print(f"🔄 Procesando proveedor individual...")
    
    try:
        # Limpiar datos antes del procesamiento
        proveedor_data = limpiar_datos_proveedor(proveedor_data)
        
        # Mapear datos de la API al formato del modelo
        mapped_data = map_proveedor_data(proveedor_data)
        
        if not mapped_data or not mapped_data.get('nit'):
            print(f"⚠️ Datos inválidos o sin NIT")
            return None, "Datos inválidos"
        
        nit = mapped_data['nit']
        
        # Usar transacción para cada proveedor
        with transaction.atomic():
            # Verificar si el proveedor ya existe
            proveedor_existente = Proveedor.objects.filter(nit=nit).first()
            
            if proveedor_existente:
                # Actualizar proveedor existente
                print(f"📝 Actualizando proveedor: {nit}")
                
                # Actualizar campos
                for field, value in mapped_data.items():
                    if hasattr(proveedor_existente, field):
                        setattr(proveedor_existente, field, value)
                
                proveedor_existente.save()
                return proveedor_existente, "Actualizado"
                
            else:
                # Crear nuevo proveedor
                print(f"➕ Creando nuevo proveedor: {nit}")
                
                nuevo_proveedor = Proveedor.objects.create(**mapped_data)
                return nuevo_proveedor, "Creado"

    except Exception as e:
        print(f"❌ Error procesando proveedor: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, f"Error: {str(e)}"

def process_proveedor_api_data(proveedores_data):
    """Procesa los datos de la API de proveedores y los guarda en la base de datos"""
    print(f"🔄 Iniciando procesamiento de {len(proveedores_data)} proveedores...")
    
    nuevos = 0
    actualizados = 0 
    errores = 0

    for data in proveedores_data:
        try:
            # Limpiar datos antes del procesamiento
            data = limpiar_datos_proveedor(data)
            
            # Mapear datos de la API al formato del modelo
            proveedor_data = map_proveedor_data(data)
            
            if not proveedor_data or not proveedor_data.get('nit'):
                print(f"⚠️ Datos inválidos o sin NIT: {data}")
                errores += 1
                continue
            
            nit = proveedor_data['nit']
            
            # Usar transacción para cada proveedor
            with transaction.atomic():
                # Verificar si el proveedor ya existe
                proveedor_existente = Proveedor.objects.filter(nit=nit).first()
                
                if proveedor_existente:
                    # Actualizar proveedor existente
                    print(f"📝 Actualizando proveedor: {nit}")
                    
                    # Actualizar campos
                    for field, value in proveedor_data.items():
                        if hasattr(proveedor_existente, field):
                            setattr(proveedor_existente, field, value)
                    
                    proveedor_existente.save()
                    actualizados += 1
                    
                else:
                    # Crear nuevo proveedor
                    print(f"➕ Creando nuevo proveedor: {nit}")
                    
                    nuevo_proveedor = Proveedor.objects.create(**proveedor_data)
                    nuevos += 1

        except Exception as e:
            print(f"❌ Error procesando proveedor {data.get('nit', 'unknown')}: {str(e)}")
            errores += 1
            continue

    print(f"✅ Procesamiento completado: {nuevos} nuevos, {actualizados} actualizados, {errores} errores")
    return nuevos, actualizados, errores