# app/docs_contractual/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from dashboard.models import Contrato
from .models import HistorialGeneracion, PlantillaDocumento
import json
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.shared import OxmlElement, qn
import os
from datetime import datetime
import tempfile
import re
import locale

# Configurar locale para fechas en español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
    except:
        pass  # Si no se puede configurar, usar nombres manuales

# Diccionario para nombres de meses en español
MESES_ESPANOL = {
    'January': 'enero', 'February': 'febrero', 'March': 'marzo',
    'April': 'abril', 'May': 'mayo', 'June': 'junio',
    'July': 'julio', 'August': 'agosto', 'September': 'septiembre',
    'October': 'octubre', 'November': 'noviembre', 'December': 'diciembre'
}

# Código de entidad (mismo que dashboard)
codigo_ent = 727001372

def formatear_fecha_espanol(fecha):
    """Formatear fecha en español"""
    if not fecha:
        return 'N/A'
    
    try:
        # Formatear fecha en inglés primero
        fecha_str = fecha.strftime('%d de %B de %Y')
        
        # Reemplazar nombres de meses en inglés por español
        for ingles, espanol in MESES_ESPANOL.items():
            fecha_str = fecha_str.replace(ingles, espanol)
        
        return fecha_str
    except:
        return fecha.strftime('%d/%m/%Y') if fecha else 'N/A'

def aplicar_formato_arial10(paragraph):
    """Aplicar formato Arial 10 a un párrafo"""
    for run in paragraph.runs:
        run.font.name = 'Arial'
        run.font.size = Pt(10)

def reemplazar_variables_en_docx(doc_path, variables):
    """
    Función para reemplazar variables en un documento Word con formato Arial 10
    
    Args:
        doc_path: Ruta al archivo .docx plantilla
        variables: Diccionario con las variables a reemplazar
    
    Returns:
        Document: Documento de python-docx con variables reemplazadas
    """
    # Abrir el documento plantilla
    doc = Document(doc_path)
    
    # Función para reemplazar texto en un párrafo
    def reemplazar_en_parrafo(paragraph):
        for variable, valor in variables.items():
            if variable in paragraph.text:
                # Reemplazar en el texto completo del párrafo
                paragraph.text = paragraph.text.replace(variable, str(valor))
                # Aplicar formato Arial 10
                aplicar_formato_arial10(paragraph)
    
    # Función para reemplazar texto en una tabla
    def reemplazar_en_tabla(table):
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    reemplazar_en_parrafo(paragraph)
    
    # Reemplazar en párrafos principales
    for paragraph in doc.paragraphs:
        reemplazar_en_parrafo(paragraph)
    
    # Reemplazar en tablas
    for table in doc.tables:
        reemplazar_en_tabla(table)
    
    # Reemplazar en headers y footers
    for section in doc.sections:
        # Header
        if section.header:
            for paragraph in section.header.paragraphs:
                reemplazar_en_parrafo(paragraph)
            for table in section.header.tables:
                reemplazar_en_tabla(table)
        
        # Footer
        if section.footer:
            for paragraph in section.footer.paragraphs:
                reemplazar_en_parrafo(paragraph)
            for table in section.footer.tables:
                reemplazar_en_tabla(table)
    
    return doc

@login_required
def docs_contractual_index(request):
    """Vista principal del módulo Docs Contractual"""
    return render(request, 'docs_contractual/index.html', {
        'title': 'Docs Contractual',
        'subtitle': 'Generación de documentos contractuales'
    })

@login_required
def buscar_contratos(request):
    """Vista AJAX para buscar contratos"""
    if request.method == 'GET':
        referencia = request.GET.get('referencia', '').strip()
        proveedor = request.GET.get('proveedor', '').strip()
        
        # Query base - solo contratos de la entidad
        queryset = Contrato.objects.filter(codigo_entidad=codigo_ent)
        
        # Aplicar filtros de búsqueda
        if referencia:
            queryset = queryset.filter(referencia_del_contrato__icontains=referencia)
        
        if proveedor:
            queryset = queryset.filter(proveedor_adjudicado__icontains=proveedor)
        
        # Si se proporcionaron ambos filtros, usar OR
        if referencia and proveedor:
            queryset = Contrato.objects.filter(
                codigo_entidad=codigo_ent
            ).filter(
                Q(referencia_del_contrato__icontains=referencia) |
                Q(proveedor_adjudicado__icontains=proveedor)
            )
        
        # Limitar resultados a 50 para mejor rendimiento
        contratos = queryset[:50]
        
        # Preparar datos para JSON
        resultados = []
        for contrato in contratos:
            resultados.append({
                'id': contrato.id,
                'referencia_del_contrato': contrato.referencia_del_contrato or '',
                'objeto_del_contrato': contrato.objeto_del_contrato or '',
                'estado_contrato': contrato.estado_contrato or '',
                'proveedor_adjudicado': contrato.proveedor_adjudicado or '',
                # Datos adicionales para el documento
                'fecha_de_firma': contrato.fecha_de_firma.strftime('%Y-%m-%d') if contrato.fecha_de_firma else '',
                'tipo_de_contrato': contrato.tipo_de_contrato or '',
                'tipodocproveedor': contrato.tipodocproveedor or '',
                'documento_proveedor': contrato.documento_proveedor or '',
                'valor_del_contrato': str(contrato.valor_del_contrato) if contrato.valor_del_contrato else '0',
                'duracion_del_contrato': contrato.duracion_del_contrato or ''
            })
        
        return JsonResponse({
            'success': True,
            'contratos': resultados,
            'total': len(resultados)
        })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
@require_POST
def generar_documento(request):
    """Vista para generar documento Word con información del contrato usando plantilla"""
    try:
        # Obtener datos del POST (form data o JSON)
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            contrato_id = data.get('contrato_id')
        else:
            # Form data
            contrato_id = request.POST.get('contrato_id')
        
        if not contrato_id:
            return JsonResponse({
                'success': False, 
                'error': 'ID de contrato requerido'
            })
        
        # Convertir a entero si es string
        try:
            contrato_id = int(contrato_id)
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False, 
                'error': 'ID de contrato inválido'
            })
        
        # Obtener el contrato
        contrato = get_object_or_404(Contrato, id=contrato_id, codigo_entidad=codigo_ent)
        
        # Ruta de la plantilla
        plantilla_path = os.path.join(
            settings.BASE_DIR, 
            'docs_contractual', 
            'templates', 
            'documents', 
            'plantilla_designacion.docx'
        )
        
        # Verificar si existe la plantilla
        if not os.path.exists(plantilla_path):
            # Si no existe plantilla, generar documento desde cero (método anterior)
            return generar_documento_sin_plantilla(contrato)
        
        # Preparar variables para reemplazar
        variables = {
            '{{w_fecha}}': formatear_fecha_espanol(contrato.fecha_de_firma),
            '{{w_contrato}}': (contrato.referencia_del_contrato or 'N/A').upper(),
            '{{w_tipo}}': (contrato.tipo_de_contrato or 'N/A').upper(),
            '{{w_contratista}}': (contrato.proveedor_adjudicado or 'N/A').upper(),
            '{{w_tipodoc}}': 'NIT' if (contrato.tipodocproveedor or '').upper() in ['NO DEFINIDO', 'N/A', ''] else contrato.tipodocproveedor.upper(),
            '{{w_id}}': (contrato.documento_proveedor or 'N/A').upper(),
            '{{w_objeto}}': (contrato.objeto_del_contrato or 'N/A').upper(),
            '{{w_valor}}': f"${contrato.valor_del_contrato:,.0f}" if contrato.valor_del_contrato else 'N/A',
            '{{w_plazo}}': (contrato.duracion_del_contrato or 'N/A').upper() if contrato.duracion_del_contrato else 'N/A'
        }
        
        # Generar documento usando plantilla
        doc = reemplazar_variables_en_docx(plantilla_path, variables)
        
        # Generar nombre del archivo
        fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
        referencia_limpia = contrato.referencia_del_contrato.replace('/', '_').replace(' ', '_') if contrato.referencia_del_contrato else 'contrato'
        nombre_archivo = f"Designacion_{referencia_limpia}_{fecha_actual}.docx"
        
        # Guardar archivo temporalmente
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
        
        # Guardar el documento en la respuesta
        doc.save(response)
        
        # Registrar en historial
        try:
            # Crear una plantilla por defecto si no existe
            plantilla, created = PlantillaDocumento.objects.get_or_create(
                nombre="Plantilla Designación",
                defaults={
                    'descripcion': 'Plantilla Word para designación de supervisor',
                    'activa': True
                }
            )
            
            HistorialGeneracion.objects.create(
                contrato_referencia=contrato.referencia_del_contrato or str(contrato.id),
                plantilla_usada=plantilla,
                usuario=request.user.username,
                nombre_archivo_generado=nombre_archivo
            )
        except Exception as e:
            print(f"Error al guardar historial: {e}")
        
        return response
        
    except Contrato.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Contrato no encontrado'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al generar documento: {str(e)}'
        })

def generar_documento_sin_plantilla(contrato):
    """Función auxiliar para generar documento sin plantilla (método anterior) con formato Arial 10"""
    # Crear documento Word desde cero
    doc = Document()
    
    # Configurar el documento
    titulo = doc.add_heading('DESIGNACIÓN DE SUPERVISOR', 0)
    aplicar_formato_arial10(titulo)
    
    # Agregar contenido del documento
    doc.add_paragraph('')  # Espacio
    
    # Párrafo de introducción
    intro = doc.add_paragraph()
    intro.add_run('En cumplimiento de lo establecido en el artículo 84 de la Ley 1474 de 2011 ')
    intro.add_run('(Estatuto Anticorrupción), se designa supervisor para el contrato que a ')
    intro.add_run('continuación se relaciona:')
    aplicar_formato_arial10(intro)
    
    doc.add_paragraph('')  # Espacio
    
    # Tabla con información del contrato
    table = doc.add_table(rows=8, cols=2)
    table.style = 'Table Grid'
    
    # Configurar datos de la tabla con formato correcto
    tipodoc_valor = 'NIT' if (contrato.tipodocproveedor or '').upper() in ['NO DEFINIDO', 'N/A', ''] else (contrato.tipodocproveedor or 'N/A').upper()
    
    datos_tabla = [
        ('FECHA DE FIRMA:', formatear_fecha_espanol(contrato.fecha_de_firma)),
        ('CONTRATO:', (contrato.referencia_del_contrato or 'N/A').upper()),
        ('TIPO:', (contrato.tipo_de_contrato or 'N/A').upper()),
        ('CONTRATISTA:', (contrato.proveedor_adjudicado or 'N/A').upper()),
        ('TIPO DOC:', tipodoc_valor),
        ('IDENTIFICACIÓN:', (contrato.documento_proveedor or 'N/A').upper()),
        ('OBJETO:', (contrato.objeto_del_contrato or 'N/A').upper()),
        ('VALOR:', f"${contrato.valor_del_contrato:,.0f}" if contrato.valor_del_contrato else 'N/A'),
    ]
    
    # Llenar la tabla
    for i, (etiqueta, valor) in enumerate(datos_tabla):
        row_cells = table.rows[i].cells
        row_cells[0].text = etiqueta
        row_cells[1].text = str(valor)
        
        # Aplicar formato Arial 10 a todas las celdas
        for cell in row_cells:
            for paragraph in cell.paragraphs:
                aplicar_formato_arial10(paragraph)
                # Hacer etiquetas en negrita
                if cell == row_cells[0]:  # Primera columna (etiquetas)
                    for run in paragraph.runs:
                        run.bold = True
    
    # Agregar plazo si existe
    if contrato.duracion_del_contrato:
        doc.add_paragraph('')
        plazo_p = doc.add_paragraph()
        plazo_run = plazo_p.add_run('PLAZO: ')
        plazo_run.bold = True
        plazo_p.add_run(str(contrato.duracion_del_contrato).upper())
        aplicar_formato_arial10(plazo_p)
    
    # Párrafo final
    doc.add_paragraph('')
    final_p = doc.add_paragraph('La presente designación se realiza de conformidad con la normatividad vigente.')
    aplicar_formato_arial10(final_p)
    
    # Firmas
    doc.add_paragraph('')
    doc.add_paragraph('')
    
    linea1 = doc.add_paragraph('_' * 40)
    aplicar_formato_arial10(linea1)
    
    ordenador = doc.add_paragraph('ORDENADOR DEL GASTO')
    aplicar_formato_arial10(ordenador)
    
    doc.add_paragraph('')
    
    linea2 = doc.add_paragraph('_' * 40)
    aplicar_formato_arial10(linea2)
    
    supervisor = doc.add_paragraph('SUPERVISOR DESIGNADO')
    aplicar_formato_arial10(supervisor)
    
    # Generar nombre del archivo
    fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
    referencia_limpia = contrato.referencia_del_contrato.replace('/', '_').replace(' ', '_') if contrato.referencia_del_contrato else 'contrato'
    nombre_archivo = f"Designacion_{referencia_limpia}_{fecha_actual}.docx"
    
    # Guardar archivo temporalmente
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    
    # Guardar el documento en la respuesta
    doc.save(response)
    
    return response

@login_required
def historial_documentos(request):
    """Vista para mostrar historial de documentos generados"""
    historial = HistorialGeneracion.objects.all().order_by('-fecha_generacion')[:100]
    
    return render(request, 'docs_contractual/historial.html', {
        'historial': historial,
        'title': 'Historial de Documentos'
    })

@login_required
def gestionar_plantillas(request):
    """Vista para gestionar plantillas de documentos"""
    # Verificar si existe la plantilla por defecto
    plantilla_path = os.path.join(
        settings.BASE_DIR, 
        'docs_contractual', 
        'templates', 
        'documents', 
        'plantilla_designacion.docx'
    )
    
    plantilla_existe = os.path.exists(plantilla_path)
    
    context = {
        'title': 'Gestión de Plantillas',
        'plantilla_existe': plantilla_existe,
        'plantilla_path': 'docs_contractual/templates/documents/plantilla_designacion.docx',
        'variables_disponibles': [
            '{{w_fecha}} - Fecha de firma del contrato (en español)',
            '{{w_contrato}} - Referencia del contrato (MAYÚSCULAS)',
            '{{w_tipo}} - Tipo de contrato (MAYÚSCULAS)',
            '{{w_contratista}} - Nombre del proveedor (MAYÚSCULAS)',
            '{{w_tipodoc}} - Tipo de documento ("No Definido" → "NIT")',
            '{{w_id}} - Número de documento del proveedor (MAYÚSCULAS)',
            '{{w_objeto}} - Objeto del contrato (MAYÚSCULAS)',
            '{{w_valor}} - Valor del contrato (formato moneda)',
            '{{w_plazo}} - Duración del contrato (MAYÚSCULAS)'
        ]
    }
    
    return render(request, 'docs_contractual/plantillas.html', context)

@login_required
def preview_variables(request, contrato_id):
    """Vista para preview de variables de un contrato específico con formato correcto"""
    try:
        contrato = get_object_or_404(Contrato, id=contrato_id, codigo_entidad=codigo_ent)
        
        # Aplicar el mismo formato que se usa en la generación real
        tipodoc_valor = 'NIT' if (contrato.tipodocproveedor or '').upper() in ['NO DEFINIDO', 'N/A', ''] else (contrato.tipodocproveedor or 'N/A').upper()
        
        variables = {
            'w_fecha': formatear_fecha_espanol(contrato.fecha_de_firma),
            'w_contrato': (contrato.referencia_del_contrato or 'N/A').upper(),
            'w_tipo': (contrato.tipo_de_contrato or 'N/A').upper(),
            'w_contratista': (contrato.proveedor_adjudicado or 'N/A').upper(),
            'w_tipodoc': tipodoc_valor,
            'w_id': (contrato.documento_proveedor or 'N/A').upper(),
            'w_objeto': (contrato.objeto_del_contrato or 'N/A').upper(),
            'w_valor': f"${contrato.valor_del_contrato:,.0f}" if contrato.valor_del_contrato else 'N/A',
            'w_plazo': (contrato.duracion_del_contrato or 'N/A').upper() if contrato.duracion_del_contrato else 'N/A'
        }
        
        return JsonResponse({
            'success': True,
            'variables': variables,
            'contrato_info': {
                'referencia': contrato.referencia_del_contrato,
                'proveedor': contrato.proveedor_adjudicado
            },
            'formato_info': {
                'fuente': 'Arial 10',
                'fecha_idioma': 'Español',
                'variables_mayusculas': 'Sí (excepto fecha)',
                'tipodoc_conversion': '"No Definido" se convierte a "NIT"'
            }
        })
        
    except Contrato.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Contrato no encontrado'
        })