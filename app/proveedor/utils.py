# app/proveedor/utils.py
import pandas as pd
from sodapy import Socrata

def api_consulta_proveedor(nit):
    """
    Consulta proveedor por NIT usando Socrata - adaptado a tu código base
    Siguiendo el patrón de dashboard/utils.py
    """
    print(f"🔍 Consultando proveedor con NIT: {nit}")
    
    # Cliente Socrata (usando el mismo token que dashboard/utils.py)
    client = Socrata("www.datos.gov.co", "OfrpoiiPaNAfK0D6jR7qcl43f")
    socrata_dataset_identifier = "qmzu-gj57"  # Dataset de proveedores RUP

    # Query adaptado del código proporcionado
    query = f"""
        SELECT *
        WHERE nit = '{nit}'
        ORDER BY nit DESC
        LIMIT 1
    """

    try:
        print(f"📡 Ejecutando consulta API Socrata...")
        
        # Realizar la consulta a la API (siguiendo tu patrón exacto)
        resultado_proveedor = client.get(socrata_dataset_identifier, content_type="json", query=query)

        # Convertir los datos a DataFrame (como en tu código)
        resultado_proveedor_df = pd.DataFrame.from_dict(resultado_proveedor)

        print(f"📊 Registros obtenidos de la API: {len(resultado_proveedor_df)}")

        # Si el DataFrame está vacío, devolver mensaje específico (siguiendo tu patrón)
        if resultado_proveedor_df.empty:
            print("⚠️ No se encontraron resultados para el NIT consultado")
            return {"status": "no_data", "message": "No se encontraron resultados para el NIT consultado."}

        # Procesar los datos (siguiendo tus patrones de limpieza)
        if not resultado_proveedor_df.empty:
            # Limpiar saltos de línea en campos de texto (como haces en dashboard)
            text_columns = ['nombre', 'direccion', 'descripcion_categoria_principal', 'ubicacion']
            for col in text_columns:
                if col in resultado_proveedor_df.columns:
                    resultado_proveedor_df[col] = resultado_proveedor_df[col].astype(str).str.replace('\n', ' ')
            
            # Establecer índice si existe código (como en tu ejemplo)
            if 'codigo' in resultado_proveedor_df.columns:
                resultado_proveedor_df.set_index('codigo', inplace=True)

        print("✅ Datos procesados correctamente")
        
        # Convertir el DataFrame a JSON y retornar con estado de éxito (tu patrón exacto)
        return {"status": "success", "data": resultado_proveedor_df.to_json(orient="records", force_ascii=False)}

    except Exception as e:
        # Manejo de errores siguiendo tu patrón
        print(f"❌ Error al realizar la consulta de proveedores: {str(e)}")
        return {"status": "error", "message": f"Error al realizar la consulta de proveedores: {str(e)}"}

def validar_nit(nit):
    """
    Validar formato básico del NIT (función auxiliar)
    """
    if not nit:
        return False
    
    # Limpiar el valor (remover espacios y guiones)
    nit_clean = str(nit).replace(' ', '').replace('-', '').replace('.', '')
    
    # Debe ser solo números y tener al menos 7 dígitos
    return nit_clean.isdigit() and len(nit_clean) >= 7 and len(nit_clean) <= 15

def api_consulta_proveedor_completa():
    """
    Función opcional para consulta masiva de proveedores (siguiendo tu patrón de api_consulta)
    Útil para sincronización masiva si se necesita
    """
    print("🚀 Iniciando consulta masiva de proveedores...")
    
    client = Socrata("www.datos.gov.co", "OfrpoiiPaNAfK0D6jR7qcl43f")
    socrata_dataset_identifier = "qmzu-gj57"

    # Query para obtener proveedores activos (ajustar según necesidad)
    query = """
        SELECT *
        WHERE esta_activa = 'true'
        ORDER BY fecha_creacion DESC
        LIMIT 1000
    """

    try:
        print("📡 Ejecutando consulta masiva...")
        
        # Realizar la consulta a la API
        proveedores_data = client.get(socrata_dataset_identifier, content_type="json", query=query)

        # Convertir los datos a DataFrame
        proveedores_df = pd.DataFrame.from_dict(proveedores_data)

        # Si el DataFrame está vacío, devolver mensaje específico
        if proveedores_df.empty:
            return {"status": "no_data", "message": "No se encontraron proveedores activos."}

        # Limpiar saltos de línea en campos de texto (tu patrón)
        text_columns = ['nombre', 'direccion', 'descripcion_categoria_principal', 'ubicacion']
        for col in text_columns:
            if col in proveedores_df.columns:
                proveedores_df[col] = proveedores_df[col].astype(str).str.replace('\n', ' ')

        # Eliminar registros duplicados por NIT (siguiendo tu patrón)
        proveedores_df = proveedores_df.drop_duplicates(subset=['nit'], keep='last')

        print(f"✅ Procesados {len(proveedores_df)} proveedores únicos")

        # Convertir el DataFrame a JSON y retornar con estado de éxito
        return {"status": "success", "data": proveedores_df.to_json(orient="records", force_ascii=False)}

    except Exception as e:
        print(f"❌ Error en consulta masiva de proveedores: {str(e)}")
        return {"status": "error", "message": f"Error en consulta masiva de proveedores: {str(e)}"}

def limpiar_datos_proveedor(proveedor_data):
    """
    Limpia y valida los datos de proveedor obtenidos de la API
    Siguiendo tus patrones de procesamiento de datos
    """
    try:
        # Campos de texto que necesitan limpieza
        text_fields = [
            'nombre', 'direccion', 'telefono', 'correo', 'sitio_web',
            'nombre_representante_legal', 'telefono_representante_legal', 
            'correo_representante_legal'
        ]
        
        for field in text_fields:
            if field in proveedor_data and proveedor_data[field]:
                # Limpiar saltos de línea y espacios extra
                proveedor_data[field] = str(proveedor_data[field]).replace('\n', ' ').strip()
        
        # Validar y limpiar NIT
        if 'nit' in proveedor_data:
            nit = str(proveedor_data['nit']).replace(' ', '').replace('-', '').replace('.', '')
            proveedor_data['nit'] = nit
        
        # Normalizar valores booleanos (como string siguiendo tu patrón)
        boolean_fields = ['es_entidad', 'es_grupo', 'esta_activa', 'espyme']
        for field in boolean_fields:
            if field in proveedor_data:
                value = str(proveedor_data[field]).lower()
                proveedor_data[field] = 'true' if value in ['true', '1', 'si', 'sí'] else 'false'
        
        return proveedor_data
        
    except Exception as e:
        print(f"⚠️ Error limpiando datos de proveedor: {str(e)}")
        return proveedor_data