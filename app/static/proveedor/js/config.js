/**
 * Configuracion del modulo de proveedores
 * Personaliza estos valores segun tu necesidad
 */

window.ProveedorConfig = {
    // URLs de la API (si usas endpoints personalizados)
    apiEndpoints: {
        consultarNit: '/proveedor/consultar-nit/',
        registrar: '/proveedor/registrar/',
        actualizar: '/proveedor/detalle/'
    },
    
    // Configuraciones de validacion
    validation: {
        nitMinLength: 7,
        nitMaxLength: 15,
        nombreMinLength: 3
    },
    
    // Mensajes personalizados
    messages: {
        nitInvalido: 'NIT invalido. Solo numeros, 7-15 digitos',
        nombreRequerido: 'El nombre es requerido',
        consultandoAPI: 'Consultando informacion del proveedor...'
    },
    
    // Configuracion de UX
    ui: {
        showLoadingSpinner: true,
        autoFocusFirstField: true,
        validateOnType: true
    }
};
