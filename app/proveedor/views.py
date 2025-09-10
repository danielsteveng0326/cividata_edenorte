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
from .utils import api_consulta_proveedor, validar_nit, api_consulta_proveedor_completa
from .db import process_single_proveedor_data, get_proveedores_stats, process_proveedor_api_data
import json
from datetime import datetime

@login_required
def index(request):
    """Vista principal del módulo de proveedores"""
    print("🚀 Accediendo al módulo de proveedores...")
    
    try:
        # Obtener estadísticas básicas
        estadisticas = get_proveedores_stats()
        print(f"📊 Estadísticas de proveedores: {estadisticas}")
        
        # Obtener último proveedor registrado
        ultimo_proveedor = Proveedor.objects.filter(activo='true').order_by('-fecha_registro').first()
        
        context = {
            'estadisticas': estadisticas,
            'ultimo_proveedor': ultimo_proveedor,
        }
        
        return render(request, 'proveedor/index.html', context)
        
    except Exception as e:
        print(f"❌ ERROR en vista index de proveedores: {e}")
        import traceback
        traceback.print_exc()
        
        return render(request, 'proveedor/index.html', {
            'error': f'Error interno: {str(e)}',
            'estadisticas': {
                'total': 0, 'activos': 0, 'inactivos': 0, 
                'pymes': 0, 'personas_naturales': 0, 'empresas': 0
            }
        })

@login_required
@require_POST
def consultar_nit(request):
    """Vista AJAX para consultar proveedor por NIT"""
    print("🔍 Iniciando consulta por NIT...")
    
    try:
        nit = request.POST.get('nit', '').strip()
        print(f"📋 NIT solicitado: {nit}")
        
        if not nit:
            print("⚠️ NIT vacío")
            return JsonResponse({
                'success': False,
                'message': 'El NIT es requerido'
            })
        
        # Validar formato de NIT
        if not validar_nit(nit):
            print(f"⚠️ NIT inválido: {nit}")
            return JsonResponse({
                'success': False,
                'message': 'Formato de NIT inválido. Solo números, entre 7 y 15 dígitos.'
            })
        
        # Primero buscar en la base de datos local
        try:
            proveedor_local = Proveedor.objects.get(nit=nit, activo='true')
            print(f"✅ Proveedor encontrado en BD local: {proveedor_local.nombre}")
            
            html_content = f"""
            <div class="row">
                <div class="col-md-6">
                    <h5><i class="fas fa-building"></i> {proveedor_local.nombre}</h5>
                    <p><strong>NIT:</strong> {proveedor_local.nit}</p>
                    <p><strong>Teléfono:</strong> {proveedor_local.telefono or 'No registrado'}</p>
                    <p><strong>Correo:</strong> {proveedor_local.correo or 'No registrado'}</p>
                    <p><strong>Dirección:</strong> {proveedor_local.direccion or 'No registrada'}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Tipo:</strong> {proveedor_local.tipo_empresa or 'No especificado'}</p>
                    <p><strong>Estado:</strong> <span class="badge badge-success">Activo</span></p>
                    <p><strong>Fecha Registro:</strong> {proveedor_local.fecha_registro.strftime('%d/%m/%Y') if proveedor_local.fecha_registro else 'N/A'}</p>
                    <div class="mt-3">
                        <a href="/proveedor/detalle/{proveedor_local.id}/" class="btn btn-info btn-sm">
                            <i class="fas fa-eye"></i> Ver Detalles
                        </a>
                    </div>
                </div>
            </div>
            """
            
            return JsonResponse({
                'success': True,
                'html': html_content,
                'source': 'local'
            })
            
        except Proveedor.DoesNotExist:
            print(f"ℹ️ Proveedor no encontrado en BD local, consultando API...")
            pass
        
        # Si no está en BD local, consultar API
        resultado_api = api_consulta_proveedor(nit)
        
        if resultado_api['status'] == 'success':
            print("✅ Proveedor encontrado en API")
            
            # Procesar datos de la API
            data_json = json.loads(resultado_api['data'])
            if data_json and len(data_json) > 0:
                proveedor_data = data_json[0]
                
                # Intentar guardar en BD local
                try:
                    proveedor_obj, accion = process_single_proveedor_data(proveedor_data)
                    if proveedor_obj:
                        print(f"✅ Proveedor {accion.lower()} en BD local")
                    
                    html_content = f"""
                    <div class="row">
                        <div class="col-md-6">
                            <h5><i class="fas fa-building"></i> {proveedor_data.get('nombre', 'N/A')}</h5>
                            <p><strong>NIT:</strong> {proveedor_data.get('nit', 'N/A')}</p>
                            <p><strong>Teléfono:</strong> {proveedor_data.get('telefono', 'No registrado')}</p>
                            <p><strong>Correo:</strong> {proveedor_data.get('correo', 'No registrado')}</p>
                            <p><strong>Dirección:</strong> {proveedor_data.get('direccion', 'No registrada')}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Tipo:</strong> {proveedor_data.get('tipo_empresa', 'No especificado')}</p>
                            <p><strong>Estado:</strong> <span class="badge badge-success">Encontrado en API</span></p>
                            <p><strong>Es PyME:</strong> {'Sí' if proveedor_data.get('espyme') == 'true' else 'No'}</p>
                            <div class="mt-3">
                                <span class="badge badge-info">Consultado desde API RUP</span>
                                {f'<br><a href="/proveedor/detalle/{proveedor_obj.id}/" class="btn btn-info btn-sm mt-2"><i class="fas fa-eye"></i> Ver Detalles</a>' if proveedor_obj else ''}
                            </div>
                        </div>
                    </div>
                    """
                    
                    return JsonResponse({
                        'success': True,
                        'html': html_content,
                        'source': 'api'
                    })
                    
                except Exception as e:
                    print(f"⚠️ Error guardando proveedor de API: {str(e)}")
                    # Aún así devolver los datos de la API
                    html_content = f"""
                    <div class="row">
                        <div class="col-md-12">
                            <h5><i class="fas fa-building"></i> {proveedor_data.get('nombre', 'N/A')}</h5>
                            <p><strong>NIT:</strong> {proveedor_data.get('nit', 'N/A')}</p>
                            <p><strong>Información:</strong> Encontrado en API pero no pudo guardarse en BD local</p>
                            <p><strong>Error:</strong> {str(e)}</p>
                        </div>
                    </div>
                    """
                    
                    return JsonResponse({
                        'success': True,
                        'html': html_content,
                        'source': 'api',
                        'warning': f'Datos obtenidos pero no guardados: {str(e)}'
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'No se encontraron datos en la respuesta de la API'
                })
        
        elif resultado_api['status'] == 'no_data':
            print(f"ℹ️ Proveedor no encontrado en la API")
            return JsonResponse({
                'success': False,
                'message': 'Proveedor no encontrado en RUP (Registro Único de Proveedores)'
            })
        
        else:
            print(f"❌ Error en consulta API: {resultado_api.get('message')}")
            return JsonResponse({
                'success': False,
                'message': f'Error consultando la API: {resultado_api.get("message", "Error desconocido")}'
            })
            
    except Exception as e:
        print(f"❌ ERROR en consulta de NIT: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return JsonResponse({
            'success': False,
            'message': f'Error interno del servidor: {str(e)}'
        })

@login_required
def detalle_proveedor(request, proveedor_id):
    """Vista para mostrar detalles de un proveedor"""
    print(f"👁️ Accediendo a detalle de proveedor ID: {proveedor_id}")
    
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    
    if request.method == 'POST':
        print("📝 Actualizando información del proveedor...")
        
        try:
            # Actualizar información básica
            proveedor.nombre = request.POST.get('nombre', '').strip()
            proveedor.telefono = request.POST.get('telefono', '').strip()
            proveedor.correo = request.POST.get('correo', '').strip()
            proveedor.direccion = request.POST.get('direccion', '').strip()
            
            # Validar campos requeridos
            if not proveedor.nombre:
                raise ValidationError('El nombre es requerido')
            
            # Actualizar tipo de empresa si se proporciona
            tipo_empresa = request.POST.get('tipo_empresa', '').strip()
            if tipo_empresa:
                proveedor.tipo_empresa = tipo_empresa
            
            # Actualizar información de representante legal si aplica
            if proveedor.necesita_representante_legal():
                proveedor.nombre_representante_legal = request.POST.get('nombre_representante_legal', '').strip()
                proveedor.n_mero_doc_representante_legal = request.POST.get('numero_doc_representante_legal', '').strip()
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
    """Vista para registrar un proveedor manualmente"""
    print("➕ Accediendo a registro manual de proveedor...")
    
    if request.method == 'POST':
        print("📝 Procesando registro manual de proveedor...")
        
        try:
            # Obtener datos del formulario
            nombre = request.POST.get('nombre', '').strip()
            nit = request.POST.get('nit', '').strip()
            telefono = request.POST.get('telefono', '').strip()
            correo = request.POST.get('correo', '').strip()
            direccion = request.POST.get('direccion', '').strip()
            tipo_empresa = request.POST.get('tipo_empresa', '').strip()
            
            # Datos de representante legal (opcional)
            nombre_rep_legal = request.POST.get('nombre_representante_legal', '').strip()
            telefono_rep_legal = request.POST.get('telefono_representante_legal', '').strip()
            correo_rep_legal = request.POST.get('correo_representante_legal', '').strip()
            
            # Validaciones básicas
            if not nombre or not nit:
                raise ValidationError('Nombre y NIT son requeridos')
            
            if not validar_nit(nit):
                raise ValidationError('Formato de NIT inválido')
            
            # Verificar si ya existe
            if Proveedor.objects.filter(nit=nit).exists():
                raise ValidationError(f'Ya existe un proveedor con NIT {nit}')
            
            # Crear proveedor
            proveedor = Proveedor.objects.create(
                nombre=nombre,
                nit=nit,
                telefono=telefono,
                correo=correo,
                direccion=direccion,
                tipo_empresa=tipo_empresa,
                nombre_representante_legal=nombre_rep_legal,
                telefono_representante_legal=telefono_rep_legal,
                correo_representante_legal=correo_rep_legal,
                activo='true'
            )
            
            print(f"✅ Proveedor registrado exitosamente: {proveedor.nit}")
            
            # SOLUCIÓN AL PROBLEMA: Usar mensajes con diferentes tipos
            messages.success(
                request, 
                f'✅ Proveedor "{nombre}" registrado exitosamente con NIT {nit}',
                extra_tags='proveedor-success'
            )
            
            # Si es una solicitud AJAX (opcional para futuras mejoras)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Proveedor {nombre} registrado exitosamente',
                    'proveedor_id': proveedor.id,
                    'redirect_url': f'/proveedor/detalle/{proveedor.id}/'
                })
            
            # Redirigir con mensaje de éxito
            return redirect('proveedor:detalle', proveedor_id=proveedor.id)
            
        except ValidationError as e:
            print(f"❌ Error de validación: {str(e)}")
            messages.error(request, str(e), extra_tags='proveedor-error')
            
            # Mantener los datos del formulario en caso de error
            context = {
                'form_data': request.POST,
                'error': str(e)
            }
            return render(request, 'proveedor/registrar.html', context)
            
        except Exception as e:
            print(f"❌ Error registrando proveedor: {str(e)}")
            import traceback
            traceback.print_exc()
            
            messages.error(
                request, 
                f'Error al registrar: {str(e)}',
                extra_tags='proveedor-error'
            )
            
            # Mantener los datos del formulario en caso de error
            context = {
                'form_data': request.POST,
                'error': str(e)
            }
            return render(request, 'proveedor/registrar.html', context)
    
    # GET request - mostrar formulario limpio
    return render(request, 'proveedor/registrar.html')

@login_required
def listar_proveedores(request):
    """Vista para listar proveedores con filtros"""
    print("📋 Accediendo a listado de proveedores...")
    
    try:
        # Parámetros de búsqueda
        search = request.GET.get('search', '').strip()
        tipo_filtro = request.GET.get('tipo', '').strip()
        
        # Query base
        proveedores = Proveedor.objects.filter(activo='true')
        
        # Aplicar filtros
        if search:
            proveedores = proveedores.filter(
                Q(nombre__icontains=search) |
                Q(nit__icontains=search) |
                Q(correo__icontains=search)
            )
        
        if tipo_filtro:
            proveedores = proveedores.filter(tipo_empresa=tipo_filtro)
        
        # Ordenar y paginar
        proveedores = proveedores.order_by('-fecha_registro')[:50]  # Limitar a 50 por ahora
        
        context = {
            'proveedores': proveedores,
            'search': search,
            'tipo_filtro': tipo_filtro,
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
    """Vista para sincronización masiva desde API"""
    print("🚀 Iniciando sincronización masiva de proveedores...")
    
    try:
        # Obtener datos de la API
        response = api_consulta_proveedor_completa()
        
        if response['status'] == 'success':
            print("✅ API de proveedores respondió exitosamente")
            
            # Convertir JSON string a lista de diccionarios
            proveedores_data = json.loads(response['data'])
            print(f"📊 Total proveedores recibidos de la API: {len(proveedores_data)}")
            
            # Procesar los datos de la API
            nuevos, actualizados, errores = process_proveedor_api_data(proveedores_data)
            
            print(f"📈 Resultados del procesamiento:")
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
            print("⚠️ No se encontraron datos en la API de proveedores")
            return render(request, 'proveedor/api.html', {
                "error": "No se encontraron proveedores nuevos en la API",
                "success": False
            })
            
        else:
            print(f"❌ Error en API de proveedores: {response.get('message')}")
            return render(request, 'proveedor/api.html', {
                "error": response['message'],
                "success": False
            })
            
    except Exception as e:
        print(f"❌ Error crítico en vista API proveedores: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return render(request, 'proveedor/api.html', {
            "error": f"Error interno del servidor: {str(e)}",
            "success": False
        })

# Class-based view
class ProveedorListView(ListView):
    """ListView para proveedores"""
    model = Proveedor
    template_name = 'proveedor/tabla_proveedores.html'
    context_object_name = 'proveedores'
    paginate_by = 50

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        """Aplicar filtros"""
        search_filtro = self.request.GET.get('search', '') or self.request.POST.get('search', '')
        tipo_filtro = self.request.GET.get('tipo', '') or self.request.POST.get('tipo', '')
        
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
            
        return queryset.order_by('-fecha_registro')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['tipo_filtro'] = self.request.GET.get('tipo', '')
        return context