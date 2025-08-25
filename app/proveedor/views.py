# app/proveedor/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.db.models import Q, Count
from .models import Proveedor
from .utils import api_consulta_proveedor, validar_nit
from .db import process_single_proveedor_data, get_proveedores_stats
import json
from datetime import datetime

@login_required
def index(request):
    """Vista principal del módulo de proveedores - siguiendo el patrón de dashboard/views.py"""
    print("🚀 Accediendo al módulo de proveedores...")
    
    try:
        # Obtener estadísticas básicas (como en dashboard)
        stats = get_proveedores_stats()
        print(f"📊 Estadísticas de proveedores: {stats}")
        
        context = {
            'titulo': 'Gestión de Proveedores',
            'descripcion': 'Consulta y registro de proveedores',
            'stats': stats
        }
        
        return render(request, 'proveedor/index.html', context)
        
    except Exception as e:
        print(f"❌ ERROR en vista index de proveedores: {e}")
        import traceback
        traceback.print_exc()
        
        return render(request, 'proveedor/index.html', {
            'titulo': 'Gestión de Proveedores',
            'error': f'Error interno: {str(e)}'
        })

@login_required
@require_POST
def consultar_nit(request):
    """Vista AJAX para consultar proveedor por NIT - siguiendo el patrón de tus APP"""
    print("🔍 Iniciando consulta por NIT...")
    
    try:
        nit = request.POST.get('nit', '').strip()
        print(f"📋 NIT solicitado: {nit}")
        
        if not nit:
            print("⚠️ NIT vacío")
            return JsonResponse({
                'success': False,
                'error': 'El NIT es requerido'
            })
        
        # Validar formato de NIT
        if not validar_nit(nit):
            print(f"⚠️ NIT inválido: {nit}")
            return JsonResponse({
                'success': False,
                'error': 'Formato de NIT inválido. Solo números, mínimo 7 dígitos.'
            })
        
        # Verificar si ya existe en nuestra base de datos (como haces en dashboard)
        proveedor_existente = Proveedor.objects.filter(nit=nit).first()
        
        if proveedor_existente:
            print(f"✅ Proveedor encontrado en BD local: {nit}")
            return JsonResponse({
                'success': True,
                'existe_local': True,
                'proveedor': proveedor_existente.get_info_basica(),
                'proveedor_id': proveedor_existente.id,
                'message': ''
            })
        
        # Consultar a través de la API (siguiendo tu patrón exacto)
        print("📡 Consultando APP de proveedores...")
        resultado_api = api_consulta_proveedor(nit)
        
        if resultado_api['status'] == 'success':
            print("✅ APP respondió exitosamente")
            
            # Convertir JSON string a lista de diccionarios (tu patrón)
            proveedores_data = json.loads(resultado_api['data'])
            print(f"📊 Registros obtenidos de la APP: {len(proveedores_data)}")
            
            if proveedores_data and len(proveedores_data) > 0:
                # Tomar el primer registro (más reciente por el ORDER BY)
                proveedor_data = proveedores_data[0]
                
                # Procesar y guardar el proveedor en BD
                proveedor = process_single_proveedor_data(proveedor_data)
                
                if proveedor:
                    print(f"✅ Proveedor procesado y guardado: {nit}")
                    return JsonResponse({
                        'success': True,
                        'existe_local': False,
                        'proveedor': proveedor.get_info_basica(),
                        'proveedor_id': proveedor.id,
                        'message': 'Proveedor consultado y guardado'
                    })
                else:
                    print(f"❌ Error procesando proveedor: {nit}")
                    return JsonResponse({
                        'success': False,
                        'error': 'Error al procesar datos del proveedor'
                    })
            else:
                print(f"❌ Proveedor no encontrado: {nit}")
                return JsonResponse({
                    'success': False,
                    'not_found': True,
                    'message': 'Proveedor no encontrado'
                })
                
        elif resultado_api['status'] == 'no_data':
            print(f"❌ No se encontraron datos para NIT: {nit}")
            return JsonResponse({
                'success': False,
                'not_found': True,
                'message': 'Proveedor no encontrado'
            })
        else:
            print(f"❌ Error en APP: {resultado_api.get('message')}")
            return JsonResponse({
                'success': False,
                'error': resultado_api['message']
            })
            
    except Exception as e:
        print(f"❌ Error crítico en consulta por NIT: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return JsonResponse({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        })

@login_required
def detalle_proveedor(request, proveedor_id):
    """Vista para mostrar y editar detalles del proveedor - siguiendo tu patrón"""
    print(f"🔍 Accediendo a detalle de proveedor ID: {proveedor_id}")
    
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    print(f"📋 Proveedor cargado: {proveedor.nombre} - {proveedor.nit}")
    
    if request.method == 'POST':
        print("📝 Procesando actualización de proveedor...")
        
        try:
            # Actualizar información del proveedor (siguiendo tu patrón de validación)
            proveedor.nombre = request.POST.get('nombre', '').strip()
            proveedor.telefono = request.POST.get('telefono', '').strip()
            proveedor.correo = request.POST.get('correo', '').strip()
            proveedor.direccion = request.POST.get('direccion', '').strip()
            proveedor.departamento = request.POST.get('departamento', '').strip()
            proveedor.municipio = request.POST.get('municipio', '').strip()
            
            # Validaciones básicas (como haces en otras vistas)
            if not proveedor.nombre:
                print("⚠️ Error: Nombre vacío")
                messages.error(request, 'El nombre es requerido')
                return render(request, 'proveedor/detalle.html', {'proveedor': proveedor})
            
            # Actualizar información de representante legal si aplica
            if proveedor.necesita_representante_legal():
                proveedor.nombre_representante_legal = request.POST.get('nombre_representante_legal', '').strip()
                proveedor.n_mero_doc_representante_legal = request.POST.get('n_mero_doc_representante_legal', '').strip()
                proveedor.telefono_representante_legal = request.POST.get('telefono_representante_legal', '').strip()
                proveedor.correo_representante_legal = request.POST.get('correo_representante_legal', '').strip()
            
            proveedor.save()
            print(f"✅ Proveedor actualizado exitosamente: {proveedor.nit}")
            messages.success(request, 'Proveedor actualizado exitosamente')
            return redirect('proveedor:detalle', proveedor_id=proveedor.id)
            
        except ValidationError as e:
            print(f"❌ Error de validación: {str(e)}")
            messages.error(request, f'Error de validación: {str(e)}')
        except Exception as e:
            print(f"❌ Error actualizando proveedor: {str(e)}")
            import traceback
            traceback.print_exc()
            messages.error(request, f'Error al actualizar: {str(e)}')
    
    context = {
        'proveedor': proveedor,
        'info_basica': proveedor.get_info_basica(),
        'necesita_rep_legal': proveedor.necesita_representante_legal()
    }
    
    return render(request, 'proveedor/detalle.html', context)

@login_required
def registrar_proveedor(request):
    """Vista para registrar un nuevo proveedor manualmente - siguiendo tu patrón"""
    print("➕ Accediendo a registro manual de proveedor...")
    
    if request.method == 'POST':
        print("📝 Procesando registro manual...")
        
        try:
            # Obtener datos del formulario
            nit = request.POST.get('nit', '').strip()
            nombre = request.POST.get('nombre', '').strip()
            telefono = request.POST.get('telefono', '').strip()
            correo = request.POST.get('correo', '').strip()
            direccion = request.POST.get('direccion', '').strip()
            tipo_empresa = request.POST.get('tipo_empresa', 'PERSONA NATURAL COLOMBIANA')
            
            print(f"📋 Datos recibidos - NIT: {nit}, Nombre: {nombre}")
            
            # Validaciones básicas (como haces en dashboard)
            if not nit or not nombre:
                print("⚠️ Error: Campos requeridos faltantes")
                messages.error(request, 'NIT y nombre son campos requeridos')
                return render(request, 'proveedor/registrar.html', {'form_data': request.POST})
            
            # Validar formato de NIT
            if not validar_nit(nit):
                print(f"⚠️ Error: NIT inválido {nit}")
                messages.error(request, 'Formato de NIT inválido')
                return render(request, 'proveedor/registrar.html', {'form_data': request.POST})
            
            # Verificar que no exista (como validas unicidad en contratos)
            if Proveedor.objects.filter(nit=nit).exists():
                print(f"⚠️ Error: NIT duplicado {nit}")
                messages.error(request, 'Ya existe un proveedor con este NIT')
                return render(request, 'proveedor/registrar.html', {'form_data': request.POST})
            
            # Crear proveedor (usando transacción como en dashboard/db.py)
            proveedor_data = {
                'nit': nit,
                'nombre': nombre,
                'telefono': telefono,
                'correo': correo,
                'direccion': direccion,
                'tipo_empresa': tipo_empresa,
                'activo': 'true'
            }
            
            # Agregar datos de representante legal si aplica
            if tipo_empresa != 'PERSONA NATURAL COLOMBIANA':
                proveedor_data.update({
                    'nombre_representante_legal': request.POST.get('nombre_representante_legal', '').strip(),
                    'n_mero_doc_representante_legal': request.POST.get('n_mero_doc_representante_legal', '').strip(),
                    'telefono_representante_legal': request.POST.get('telefono_representante_legal', '').strip(),
                    'correo_representante_legal': request.POST.get('correo_representante_legal', '').strip(),
                })
            
            with transaction.atomic():
                proveedor = Proveedor.objects.create(**proveedor_data)
                
            print(f"✅ Proveedor registrado exitosamente: {nombre} - {nit}")
            messages.success(request, f'Proveedor {nombre} registrado exitosamente')
            return redirect('proveedor:detalle', proveedor_id=proveedor.id)
            
        except ValidationError as e:
            print(f"❌ Error de validación en registro: {str(e)}")
            messages.error(request, f'Error de validación: {str(e)}')
        except Exception as e:
            print(f"❌ Error registrando proveedor: {str(e)}")
            import traceback
            traceback.print_exc()
            messages.error(request, f'Error al registrar: {str(e)}')
            
        return render(request, 'proveedor/registrar.html', {'form_data': request.POST})
    
    return render(request, 'proveedor/registrar.html', {})

@login_required  
def listar_proveedores(request):
    """Vista para listar todos los proveedores - siguiendo el patrón de ContratoListView"""
    print("📋 Accediendo a lista de proveedores...")
    
    try:
        # Query base (como en dashboard)
        proveedores = Proveedor.objects.filter(activo='true').order_by('-fecha_registro')
        
        # Búsqueda simple (siguiendo tu patrón de filtros)
        search = request.GET.get('search', '').strip()
        if search:
            print(f"🔍 Aplicando filtro de búsqueda: {search}")
            proveedores = proveedores.filter(
                Q(nombre__icontains=search) |
                Q(nit__icontains=search)
            )
        
        # Filtro por tipo de empresa
        tipo_filtro = request.GET.get('tipo', '').strip()
        if tipo_filtro:
            print(f"🔍 Aplicando filtro de tipo: {tipo_filtro}")
            proveedores = proveedores.filter(tipo_empresa=tipo_filtro)
        
        # Filtro por estado
        estado_filtro = request.GET.get('estado', '').strip()
        if estado_filtro:
            print(f"🔍 Aplicando filtro de estado: {estado_filtro}")
            proveedores = proveedores.filter(esta_activa=estado_filtro)
        
        print(f"📊 Total proveedores encontrados: {proveedores.count()}")
        
        context = {
            'proveedores': proveedores,
            'search': search,
            'tipo_filtro': tipo_filtro,
            'estado_filtro': estado_filtro
        }
        
        return render(request, 'proveedor/listar.html', context)
        
    except Exception as e:
        print(f"❌ ERROR en vista listar proveedores: {e}")
        import traceback
        traceback.print_exc()
        
        return render(request, 'proveedor/listar.html', {
            'error': f'Error interno: {str(e)}',
            'proveedores': Proveedor.objects.none()
        })

@login_required
def api_proveedores(request):
    """Vista para sincronización masiva desde - siguiendo el patrón de dashboard ()"""
    print("🚀 Iniciando sincronización masiva de proveedores...")
    
    try:
        # Obtener datos de la API (siguiendo tu patrón exacto)
        from .utils import api_consulta_proveedor_completa
        response = api_consulta_proveedor_completa()
        
        if response['status'] == 'success':
            print("✅ APP de proveedores respondió exitosamente")
            
            # Convertir JSON string a lista de diccionarios (tu patrón)
            proveedores_data = json.loads(response['data'])
            print(f"📊 Total proveedores recibidos de la APP: {len(proveedores_data)}")
            
            # Procesar los datos de la API
            from .db import process_proveedor_api_data
            nuevos, actualizados, errores = process_proveedor_api_data(proveedores_data)
            
            print(f"📈 Resultados del procesamiento de proveedores:")
            print(f"   - Nuevos: {nuevos}")
            print(f"   - Actualizados: {actualizados}")
            print(f"   - Errores: {errores}")
            
            # Obtener la lista actualizada
            list_proveedores = Proveedor.objects.filter(activo='true').order_by('-fecha_registro')[:50]
            
            return render(request, 'proveedor/api.html', {
                "list": list_proveedores,
                "db_response": (nuevos, actualizados, errores),
                "success": True,
                "total_procesados": len(proveedores_data),
                "message": f"Procesamiento completado: {nuevos} nuevos, {actualizados} actualizados, {errores} errores"
            })
            
        elif response['status'] == 'no_data':
            print("⚠️ No se encontraron datos en la APP de proveedores")
            return render(request, 'proveedor/api.html', {
                "error": "No se encontraron proveedores nuevos en la APP",
                "success": False
            })
            
        else:
            print(f"❌ Error en APP de proveedores: {response.get('message')}")
            return render(request, 'proveedor/api.html', {
                "error": response['message'],
                "success": False
            })
            
    except Exception as e:
        print(f"❌ Error crítico en vista APP proveedores: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return render(request, 'proveedor/api.html', {
            "error": f"Error interno del servidor: {str(e)}",
            "success": False
        })

# Class-based view siguiendo el patrón de ContratoListView
class ProveedorListView(ListView):
    """ListView para proveedores siguiendo el patrón de ContratoListView"""
    model = Proveedor
    template_name = 'proveedor/tabla_proveedores.html'
    context_object_name = 'proveedores'
    paginate_by = 50  # Como en dashboard

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        """Aplicar filtros como en ContratoListView"""
        # Parámetros de filtro desde GET y POST
        search_filtro = self.request.GET.get('search', '') or self.request.POST.get('search', '')
        tipo_filtro = self.request.GET.get('tipo', '') or self.request.POST.get('tipo', '')
        estado_filtro = self.request.GET.get('estado', '') or self.request.POST.get('estado', '')
        
        # Query base
        queryset = Proveedor.objects.filter(activo='true')
        
        # Aplicar filtros
        if search_filtro:
            queryset = queryset.filter(
                Q(nombre__icontains=search_filtro) |
                Q(nit__icontains=search_filtro)
            )
        
        if tipo_filtro:
            queryset = queryset.filter(tipo_empresa=tipo_filtro)
        
        if estado_filtro:
            queryset = queryset.filter(esta_activa=estado_filtro)
            
        return queryset.order_by('-fecha_registro')