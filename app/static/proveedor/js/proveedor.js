/**
 * JavaScript para el módulo de proveedores con notificaciones mejoradas
 */

$(document).ready(function() {
    console.log('🚀 Módulo de proveedores cargado');
    
    // Configurar CSRF token para todas las peticiones AJAX
    const csrftoken = $('[name=csrfmiddlewaretoken]').val() || $('meta[name="csrf-token"]').attr('content');
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // ==========================================
    // FUNCIONES DE NOTIFICACIÓN MEJORADAS
    // ==========================================
    
    function mostrarNotificacion(tipo, titulo, mensaje, autoHide = true) {
        const iconos = {
            'success': 'fas fa-check-circle',
            'error': 'fas fa-exclamation-triangle', 
            'warning': 'fas fa-exclamation-circle',
            'info': 'fas fa-info-circle'
        };
        
        const colores = {
            'success': 'alert-success',
            'error': 'alert-danger',
            'warning': 'alert-warning', 
            'info': 'alert-info'
        };
        
        const alertHtml = `
            <div class="alert ${colores[tipo]} alert-dismissible fade show" role="alert" style="position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div class="d-flex align-items-center">
                    <i class="${iconos[tipo]} fa-lg mr-3"></i>
                    <div>
                        <h6 class="mb-1">${titulo}</h6>
                        <p class="mb-0">${mensaje}</p>
                    </div>
                </div>
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        `;
        
        $('body').append(alertHtml);
        
        if (autoHide) {
            setTimeout(() => {
                $('.alert:last').fadeOut('slow', function() {
                    $(this).remove();
                });
            }, 5000);
        }
    }
    
    function mostrarModal(tipo, titulo, mensaje, callback = null) {
        const iconos = {
            'success': 'text-success fas fa-check-circle',
            'error': 'text-danger fas fa-exclamation-triangle',
            'warning': 'text-warning fas fa-exclamation-circle',
            'info': 'text-info fas fa-info-circle'
        };
        
        const modalHtml = `
            <div class="modal fade" id="dynamicModal" tabindex="-1" role="dialog">
                <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="${iconos[tipo]} mr-2"></i>${titulo}
                            </h5>
                            <button type="button" class="close" data-dismiss="modal">
                                <span>&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <p>${mensaje}</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>
                            ${callback ? '<button type="button" class="btn btn-primary" id="modalCallback">Continuar</button>' : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remover modal existente si existe
        $('#dynamicModal').remove();
        
        $('body').append(modalHtml);
        $('#dynamicModal').modal('show');
        
        if (callback) {
            $('#modalCallback').on('click', function() {
                $('#dynamicModal').modal('hide');
                callback();
            });
        }
        
        $('#dynamicModal').on('hidden.bs.modal', function() {
            $(this).remove();
        });
    }

    // ==========================================
    // CONSULTA POR NIT MEJORADA
    // ==========================================
    
    let isSearching = false;
    
    function buscarProveedorPorNit() {
        if (isSearching) {
            console.log('⏳ Búsqueda ya en progreso...');
            return;
        }

        const nit = $('#nit-input').val().trim();
        
        // Validaciones
        if (!nit) {
            mostrarModal('warning', 'Campo requerido', 'Por favor ingrese un NIT para buscar.');
            $('#nit-input').focus();
            return;
        }

        if (!/^\d{7,15}$/.test(nit)) {
            mostrarModal('error', 'NIT inválido', 'El NIT debe contener solo números y tener entre 7 y 15 dígitos.');
            $('#nit-input').focus().select();
            return;
        }

        isSearching = true;
        const $searchBtn = $('#search-btn');
        const originalText = $searchBtn.html();
        
        // Cambiar botón a estado de carga
        $searchBtn.html('<i class="fas fa-spinner fa-spin"></i> Buscando...').prop('disabled', true);
        $('#search-results').html('<div class="text-center"><i class="fas fa-spinner fa-spin fa-2x text-primary"></i><p class="mt-2">Consultando información del proveedor...</p></div>');

        $.post('/proveedor/consultar-nit/', {
            'nit': nit,
            'csrfmiddlewaretoken': csrftoken
        })
        .done(function(response) {
            console.log('✅ Respuesta recibida:', response);
            
            if (response.success) {
                $('#search-results').html(response.html);
                
                const fuente = response.source === 'local' ? 'base de datos local' : 'API del RUP';
                mostrarNotificacion('success', '¡Proveedor encontrado!', `Información obtenida desde ${fuente}`);
                
                if (response.warning) {
                    mostrarNotificacion('warning', 'Advertencia', response.warning);
                }
            } else {
                $('#search-results').html(`
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle mr-2"></i>
                        <strong>No encontrado:</strong> ${response.message}
                    </div>
                `);
                mostrarNotificacion('info', 'Sin resultados', response.message);
            }
        })
        .fail(function(xhr, status, error) {
            console.error('❌ Error en consulta:', error);
            
            let errorMsg = 'Error de conexión. Verifique su conexión a internet.';
            
            if (xhr.responseJSON && xhr.responseJSON.message) {
                errorMsg = xhr.responseJSON.message;
            } else if (xhr.status === 500) {
                errorMsg = 'Error interno del servidor. Contacte al administrador.';
            } else if (xhr.status === 403) {
                errorMsg = 'No tiene permisos para realizar esta acción.';
            }
            
            $('#search-results').html(`
                <div class="alert alert-danger">
                    <i class="fas fa-times-circle mr-2"></i>
                    <strong>Error:</strong> ${errorMsg}
                </div>
            `);
            
            mostrarModal('error', 'Error de consulta', errorMsg);
        })
        .always(function() {
            // Restaurar botón
            $searchBtn.html(originalText).prop('disabled', false);
            isSearching = false;
        });
    }

    // Event listeners para búsqueda
    $(document).on('click', '#search-btn', buscarProveedorPorNit);
    
    $(document).on('keypress', '#nit-input', function(e) {
        if (e.which === 13) { // Enter
            e.preventDefault();
            buscarProveedorPorNit();
        }
    });

    // ==========================================
    // REGISTRO MANUAL MEJORADO
    // ==========================================
    
    // Validación en tiempo real para el formulario de registro
    $('#registrar-form').on('submit', function(e) {
        console.log('📝 Validando formulario de registro...');
        
        const nombre = $('#nombre').val().trim();
        const nit = $('#nit').val().trim();
        
        // Validaciones básicas
        if (!nombre) {
            e.preventDefault();
            mostrarModal('error', 'Campo requerido', 'El nombre de la empresa es obligatorio.');
            $('#nombre').focus();
            return false;
        }
        
        if (!nit) {
            e.preventDefault();
            mostrarModal('error', 'Campo requerido', 'El NIT es obligatorio.');
            $('#nit').focus();
            return false;
        }
        
        if (!/^\d{7,15}$/.test(nit)) {
            e.preventDefault();
            mostrarModal('error', 'NIT inválido', 'El NIT debe contener solo números y tener entre 7 y 15 dígitos.');
            $('#nit').focus().select();
            return false;
        }
        
        // Cambiar botón a estado de carga
        const $submitBtn = $('#btnRegistrar');
        const originalText = $submitBtn.html();
        $submitBtn.html('<i class="fas fa-spinner fa-spin"></i> Registrando...').prop('disabled', true);
        
        // Mostrar indicador de carga
        mostrarNotificacion('info', 'Procesando...', 'Registrando proveedor en el sistema...');
        
        // El formulario continuará con el submit normal
        return true;
    });
    
    // Validación de NIT en tiempo real
    $('#nit').on('input', function() {
        const nit = $(this).val().replace(/\D/g, ''); // Solo números
        $(this).val(nit);
        
        if (nit.length > 0 && (nit.length < 7 || nit.length > 15)) {
            $(this).addClass('is-invalid');
            if (!$(this).next('.invalid-feedback').length) {
                $(this).after('<div class="invalid-feedback">El NIT debe tener entre 7 y 15 dígitos</div>');
            }
        } else {
            $(this).removeClass('is-invalid');
            $(this).next('.invalid-feedback').remove();
        }
    });
    
    // Limpiar formulario
    $(document).on('click', '#btn-limpiar-form', function() {
        mostrarModal('info', 'Confirmar', '¿Está seguro que desea limpiar el formulario?', function() {
            $('#registrar-form')[0].reset();
            $('.is-invalid').removeClass('is-invalid');
            $('.invalid-feedback').remove();
            $('#nombre').focus();
            mostrarNotificacion('info', 'Formulario limpio', 'Puede ingresar nueva información');
        });
    });

    // ==========================================
    // FUNCIONES ADICIONALES
    // ==========================================
    
    // Auto-ocultar mensajes de Django
    setTimeout(function() {
        $('.alert.auto-hide-alert').fadeOut('slow');
    }, 5000);
    
    // Mejorar UX de campos requeridos
    $('input[required], select[required]').on('blur', function() {
        if (!$(this).val().trim()) {
            $(this).addClass('is-invalid');
        } else {
            $(this).removeClass('is-invalid');
        }
    });
    
    // Función para validar email
    $('input[type="email"]').on('blur', function() {
        const email = $(this).val().trim();
        if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            $(this).addClass('is-invalid');
            if (!$(this).next('.invalid-feedback').length) {
                $(this).after('<div class="invalid-feedback">Ingrese un correo válido</div>');
            }
        } else {
            $(this).removeClass('is-invalid');
            $(this).next('.invalid-feedback').remove();
        }
    });
    
    console.log('✅ Módulo de proveedores inicializado correctamente');
});