import pandas as pd
from sodapy import Socrata

def api_consulta():
    client = Socrata("www.datos.gov.co", "Mt36QkOr3SVBoh78nQAnJfjPG")
    socrata_dataset_identifier = "jbjy-vk9h"

    query = """
        SELECT *
        WHERE fecha_de_firma >= '2024-01-01' AND nit_entidad = '901831522'
        LIMIT 1000
    """

    try:
        # Realizar la consulta a la API
        contratos_2024_secopII = client.get(socrata_dataset_identifier, content_type="json", query=query)

        # Convertir los datos a DataFrame
        contratos_2024_secopII_DF = pd.DataFrame.from_dict(contratos_2024_secopII)

        # Si el DataFrame está vacío, devolver un mensaje específico
        if contratos_2024_secopII_DF.empty:
            return {"status": "no_data", "message": "No se encontraron resultados para la consulta."}

        # Limpiar saltos de línea en ciertas columnas
        contratos_2024_secopII_DF['objeto_del_contrato'] = contratos_2024_secopII_DF['objeto_del_contrato'].str.replace('\n', ' ')
        contratos_2024_secopII_DF['descripcion_del_proceso'] = contratos_2024_secopII_DF['descripcion_del_proceso'].str.replace('\n', ' ')

        # Eliminar registros duplicados en 'proceso_de_compra'
        contratos_2024_secopII_DF = contratos_2024_secopII_DF.drop_duplicates(subset=['proceso_de_compra'], keep='last')

        # Convertir el DataFrame a JSON y retornar con un estado de éxito
        return {"status": "success", "data": contratos_2024_secopII_DF.to_json(orient="records", force_ascii=False)}

    except Exception as e:
        # Manejo de errores si falla la consulta
        return {"status": "error", "message": f"Error al realizar la consulta: {str(e)}"}

def api_consulta_interadministrativos():
    """
    Consulta la API de SECOP para contratos interadministrativos
    """
    client = Socrata("www.datos.gov.co", "OfrpoiiPaNAfK0D6jR7qcl43f")
    socrata_dataset_identifier = "rpmr-utcd"  # Dataset para interadministrativos

    query = """
        SELECT *
        WHERE documento_proveedor = '901831522' and fecha_de_firma_del_contrato >= '2024-01-01'
        ORDER BY fecha_de_firma_del_contrato DESC
        LIMIT 1000000
    """

    try:
        # Realizar la consulta a la API
        contratos_interadmin = client.get(socrata_dataset_identifier, content_type="json", query=query)

        # Convertir los datos a DataFrame
        contratos_interadmin_df = pd.DataFrame.from_dict(contratos_interadmin)

        # Si el DataFrame está vacío, devolver un mensaje específico
        if contratos_interadmin_df.empty:
            return {"status": "no_data", "message": "No se encontraron resultados para la consulta de interadministrativos."}

        # Limpiar saltos de línea en ciertas columnas si existen
        if 'objeto_del_contrato' in contratos_interadmin_df.columns:
            contratos_interadmin_df['objeto_del_contrato'] = contratos_interadmin_df['objeto_del_contrato'].str.replace('\n', ' ')
        
        if 'objeto_a_contratar' in contratos_interadmin_df.columns:
            contratos_interadmin_df['objeto_a_contratar'] = contratos_interadmin_df['objeto_a_contratar'].str.replace('\n', ' ')

        # Eliminar registros duplicados en 'numero_de_proceso'
        contratos_interadmin_df = contratos_interadmin_df.drop_duplicates(subset=['numero_de_proceso'], keep='last')

        # Convertir el DataFrame a JSON y retornar con un estado de éxito
        return {"status": "success", "data": contratos_interadmin_df.to_json(orient="records", force_ascii=False)}

    except Exception as e:
        # Manejo de errores si falla la consulta
        return {"status": "error", "message": f"Error al realizar la consulta de interadministrativos: {str(e)}"}
