import os
import re
import logging
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from docx import Document
from docx.shared import Pt
import google.generativeai as genai
from pathlib import Path

# Configurar logger
logger = logging.getLogger(__name__)


@login_required
def index(request):
    """Vista principal para generar certificado PAA"""
    return render(request, 'paa/index.html')


@login_required
@csrf_exempt
def generar_certificado(request):
    """Procesa el estudio previo y genera el certificado PAA"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    if 'estudio_previo' not in request.FILES:
        return JsonResponse({'error': 'No se ha cargado ningún archivo'}, status=400)
    
    try:
        # Obtener el archivo cargado
        estudio_previo = request.FILES['estudio_previo']
        
        # Validar que sea un archivo .docx
        if not estudio_previo.name.endswith('.docx'):
            return JsonResponse({'error': 'El archivo debe ser un documento Word (.docx)'}, status=400)
        
        # Leer el contenido del estudio previo
        try:
            doc_estudio = Document(estudio_previo)
            texto_estudio = '\n'.join([para.text for para in doc_estudio.paragraphs])
        except Exception as e:
            return JsonResponse({'error': f'Error al leer el documento: {str(e)}'}, status=400)
        
        # Extraer información usando Gemini
        try:
            info_extraida = extraer_informacion_con_gemini(texto_estudio)
        except Exception as e:
            return JsonResponse({'error': f'Error al procesar con Gemini: {str(e)}'}, status=500)
        
        # Obtener información del usuario
        user = request.user
        
        # Determinar género automáticamente (por defecto EL)
        # Si el usuario tiene first_name, intentar detectar género común
        genero = 'EL'  # Por defecto masculino
        if hasattr(user, 'first_name') and user.first_name:
            nombre = user.first_name.lower()
            # Nombres femeninos comunes terminan en 'a'
            if nombre.endswith('a') and not nombre.endswith('ia'):
                genero = 'LA'
        
        # Cargo por defecto
        cargo = 'PROFESIONAL UNIVERSITARIO'
        
        # Preparar datos para reemplazar
        datos = {
            'w_gen': genero,
            'w_cargo': cargo,
            'w_anno': str(datetime.now().year),
            'w_codigos': info_extraida.get('codigos', ''),
            'w_objeto': info_extraida.get('objeto', ''),
            'w_valor': info_extraida.get('valor', ''),
            'w_plazo': info_extraida.get('plazo', ''),
            'w_fecha': generar_fecha_en_letras()
        }
        
        # Generar el certificado
        try:
            certificado = generar_documento_paa(datos)
        except FileNotFoundError as e:
            return JsonResponse({'error': 'No se encontró la plantilla PAA. Por favor, coloque el archivo plantilla_paa.docx en la carpeta correcta.'}, status=500)
        except Exception as e:
            return JsonResponse({'error': f'Error al generar el certificado: {str(e)}'}, status=500)
        
        # Preparar respuesta
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = f'attachment; filename="Certificado_PAA_{datetime.now().strftime("%Y%m%d_%H%M%S")}.docx"'
        certificado.save(response)
        
        return response
        
    except Exception as e:
        # Log detallado del error
        logger.error(f"Error en generar_certificado: {str(e)}", exc_info=True)
        import traceback
        error_detail = traceback.format_exc()
        print(f"ERROR DETALLADO:\n{error_detail}")
        return JsonResponse({'error': f'Error al procesar el documento: {str(e)}'}, status=500)


def extraer_informacion_con_gemini(texto_estudio):
    """Extrae información del estudio previo usando Gemini 2.5 Flash"""
    
    # Configurar Gemini con la API key desde settings
    api_key = getattr(settings, 'GEMINI_API_KEY', None) or os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError('No se ha configurado la variable de entorno GEMINI_API_KEY. Por favor, configure GEMINI_API_KEY en las variables de entorno del sistema.')
    
    genai.configure(api_key=api_key)
    
    # Usar el modelo Gemini 2.5 Flash
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Prompt para extraer información
    prompt = f"""
Analiza el siguiente estudio previo y extrae ÚNICAMENTE la siguiente información en formato JSON:

1. **objeto**: El objeto principal del contrato (descripción completa en MAYÚSCULAS)
2. **valor**: El valor estimado del contrato (solo el número, sin símbolos)
3. **plazo**: El plazo o duración del contrato (en el formato que aparezca: días, meses, etc.)
4. **codigos**: Los códigos UNSPSC mencionados o inferidos según la descripción técnica (separados por coma)

IMPORTANTE:
- Extrae el texto EXACTAMENTE como aparece
- Si hay varios objetos, selecciona el principal
- Los códigos UNSPSC deben estar separados por coma
- Limpia el texto de saltos de línea innecesarios y doble espacios
- Devuelve SOLO un objeto JSON válido, sin texto adicional

ESTUDIO PREVIO:
{texto_estudio}

Responde ÚNICAMENTE con un JSON en este formato:
{{
    "objeto": "TEXTO DEL OBJETO",
    "valor": "123456789",
    "plazo": "12 MESES",
    "codigos": "12345678, 87654321"
}}
"""
    
    # Generar respuesta
    response = model.generate_content(prompt)
    texto_respuesta = response.text.strip()
    
    # Limpiar la respuesta para obtener solo el JSON
    # Remover markdown code blocks si existen
    texto_respuesta = re.sub(r'```json\s*', '', texto_respuesta)
    texto_respuesta = re.sub(r'```\s*', '', texto_respuesta)
    texto_respuesta = texto_respuesta.strip()
    
    # Parsear JSON
    import json
    try:
        info = json.loads(texto_respuesta)
    except json.JSONDecodeError:
        # Si falla el parsing, intentar extraer manualmente
        info = {
            'objeto': 'NO IDENTIFICADO',
            'valor': '0',
            'plazo': 'NO ESPECIFICADO',
            'codigos': ''
        }
    
    return info


def generar_fecha_en_letras():
    """Genera la fecha actual en formato de letras en español"""
    meses = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    
    hoy = datetime.now()
    dia = hoy.day
    mes = meses[hoy.month]
    año = hoy.year
    
    # Convertir número a letras (simplificado para días 1-31)
    numeros = {
        1: 'uno', 2: 'dos', 3: 'tres', 4: 'cuatro', 5: 'cinco',
        6: 'seis', 7: 'siete', 8: 'ocho', 9: 'nueve', 10: 'diez',
        11: 'once', 12: 'doce', 13: 'trece', 14: 'catorce', 15: 'quince',
        16: 'dieciséis', 17: 'diecisiete', 18: 'dieciocho', 19: 'diecinueve',
        20: 'veinte', 21: 'veintiuno', 22: 'veintidós', 23: 'veintitrés',
        24: 'veinticuatro', 25: 'veinticinco', 26: 'veintiséis', 27: 'veintisiete',
        28: 'veintiocho', 29: 'veintinueve', 30: 'treinta', 31: 'treinta y uno'
    }
    
    dia_letras = numeros.get(dia, str(dia))
    
    return f"el {dia_letras} ({dia}) días del mes de {mes} de {año}"


def generar_documento_paa(datos):
    """Genera el documento PAA reemplazando los campos en la plantilla"""
    
    # Ruta a la plantilla
    base_dir = Path(__file__).resolve().parent
    plantilla_path = base_dir / 'templates' / 'paa' / 'plantilla_paa.docx'
    
    if not plantilla_path.exists():
        raise FileNotFoundError(f'No se encontró la plantilla en: {plantilla_path}')
    
    # Cargar la plantilla
    doc = Document(str(plantilla_path))
    
    # Reemplazar en párrafos
    for para in doc.paragraphs:
        for key, value in datos.items():
            placeholder = '{{' + key + '}}'
            if placeholder in para.text:
                # Reemplazar manteniendo el formato
                for run in para.runs:
                    if placeholder in run.text:
                        run.text = run.text.replace(placeholder, str(value))
    
    # Reemplazar en tablas
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for key, value in datos.items():
                        placeholder = '{{' + key + '}}'
                        if placeholder in para.text:
                            for run in para.runs:
                                if placeholder in run.text:
                                    run.text = run.text.replace(placeholder, str(value))
    
    # Reemplazar en encabezados y pies de página
    for section in doc.sections:
        # Encabezado
        header = section.header
        for para in header.paragraphs:
            for key, value in datos.items():
                placeholder = '{{' + key + '}}'
                if placeholder in para.text:
                    for run in para.runs:
                        if placeholder in run.text:
                            run.text = run.text.replace(placeholder, str(value))
        
        # Pie de página
        footer = section.footer
        for para in footer.paragraphs:
            for key, value in datos.items():
                placeholder = '{{' + key + '}}'
                if placeholder in para.text:
                    for run in para.runs:
                        if placeholder in run.text:
                            run.text = run.text.replace(placeholder, str(value))
    
    return doc
