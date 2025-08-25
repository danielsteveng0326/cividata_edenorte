#!/usr/bin/env python3
"""
Script de instalación automatizada para el Módulo de Proveedores
Este script configura automáticamente el módulo en tu proyecto Django
"""

import os
import sys
import re
from pathlib import Path

class ProveedorModuleInstaller:
    def __init__(self, project_path='.'):
        self.project_path = Path(project_path)
        self.app_path = self.project_path / 'app'
        self.proveedor_path = self.app_path / 'proveedor'
        self.templates_path = self.app_path / 'templates' / 'proveedor'
        self.static_path = self.app_path / 'static' / 'proveedor'
        
    def print_step(self, step, message):
        print(f"\n{'='*60}")
        print(f"PASO {step}: {message}")
        print('='*60)
    
    def create_directories(self):
        """Crear estructura de directorios"""
        self.print_step(1, "Creando estructura de directorios")
        
        directories = [
            self.proveedor_path,
            self.proveedor_path / 'migrations',
            self.templates_path,
            self.static_path / 'js',
            self.static_path / 'css'
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ Creado: {directory}")
    
    def create_init_files(self):
        """Crear archivos __init__.py necesarios"""
        self.print_step(2, "Creando archivos de inicialización")
        
        init_files = [
            self.proveedor_path / '__init__.py',
            self.proveedor_path / 'migrations' / '__init__.py'
        ]
        
        for init_file in init_files:
            if not init_file.exists():
                init_file.write_text('# Auto-generated __init__.py\n')
                print(f"✅ Creado: {init_file}")
    
    def check_django_project(self):
        """Verificar que es un proyecto Django válido"""
        self.print_step(3, "Verificando proyecto Django")
        
        manage_py = self.app_path / 'manage.py'
        settings_py = self.app_path / 'app' / 'settings.py'
        
        if not manage_py.exists():
            print("❌ No se encontró manage.py")
            return False
        
        if not settings_py.exists():
            print("❌ No se encontró settings.py")
            return False
        
        print("✅ Proyecto Django válido detectado")
        return True
    
    def update_settings(self):
        """Actualizar settings.py para incluir la app proveedor"""
        self.print_step(4, "Actualizando settings.py")
        
        settings_path = self.app_path / 'app' / 'settings.py'
        
        if not settings_path.exists():
            print("❌ No se encontró settings.py")
            return False
        
        content = settings_path.read_text(encoding='utf-8')
        
        # Verificar si ya está agregado
        if "'proveedor'" in content:
            print("✅ La app 'proveedor' ya está en INSTALLED_APPS")
            return True
        
        # Buscar INSTALLED_APPS y agregar proveedor
        pattern = r'(INSTALLED_APPS\s*=\s*\[.*?)(])'
        
        def replace_installed_apps(match):
            apps_content = match.group(1)
            closing_bracket = match.group(2)
            
            # Agregar proveedor antes del closing bracket
            if not apps_content.strip().endswith(','):
                apps_content += ','
            
            return f"{apps_content}\n    'proveedor',{closing_bracket}"
        
        updated_content = re.sub(pattern, replace_installed_apps, content, flags=re.DOTALL)
        
        if updated_content != content:
            # Hacer backup
            backup_path = settings_path.with_suffix('.py.backup')
            settings_path.rename(backup_path)
            print(f"📋 Backup creado: {backup_path}")
            
            # Escribir archivo actualizado
            settings_path.write_text(updated_content, encoding='utf-8')
            print("✅ settings.py actualizado con 'proveedor' app")
        else:
            print("⚠️  No se pudo actualizar settings.py automáticamente")
            print("   Por favor agrega manualmente 'proveedor' a INSTALLED_APPS")
        
        return True
    
    def update_main_urls(self):
        """Actualizar urls.py principal para incluir rutas de proveedor"""
        self.print_step(5, "Actualizando URLs principales")
        
        urls_path = self.app_path / 'app' / 'urls.py'
        
        if not urls_path.exists():
            print("❌ No se encontró urls.py principal")
            return False
        
        content = urls_path.read_text(encoding='utf-8')
        
        # Verificar si ya está agregado
        if "proveedor.urls" in content:
            print("✅ Las URLs de proveedor ya están configuradas")
            return True
        
        # Agregar import si no existe
        if "from django.urls import path, include" not in content:
            content = content.replace(
                "from django.urls import path",
                "from django.urls import path, include"
            )
        
        # Buscar urlpatterns y agregar ruta
        pattern = r'(urlpatterns\s*=\s*\[.*?)(])'
        
        def replace_urlpatterns(match):
            patterns_content = match.group(1)
            closing_bracket = match.group(2)
            
            # Agregar ruta de proveedor
            new_pattern = "\n    path('proveedor/', include('proveedor.urls')),"
            
            return f"{patterns_content}{new_pattern}{closing_bracket}"
        
        updated_content = re.sub(pattern, replace_urlpatterns, content, flags=re.DOTALL)
        
        if updated_content != content:
            # Hacer backup
            backup_path = urls_path.with_suffix('.py.backup')
            urls_path.rename(backup_path)
            print(f"📋 Backup creado: {backup_path}")
            
            # Escribir archivo actualizado
            urls_path.write_text(updated_content, encoding='utf-8')
            print("✅ urls.py actualizado con rutas de proveedor")
        else:
            print("⚠️  No se pudo actualizar urls.py automáticamente")
            print("   Por favor agrega manualmente: path('proveedor/', include('proveedor.urls'))")
        
        return True
    
    def create_placeholder_files(self):
        """Crear archivos placeholder para que el usuario complete"""
        self.print_step(6, "Creando archivos placeholder")
        
        # Archivo utils.py con placeholder para API
        utils_content = '''"""
Funciones para consulta de proveedores a través de API externa

INSTRUCCIONES IMPORTANTES:
1. Reemplaza la función consultar_proveedor_api() con tu código de API real
2. La función debe retornar el formato especificado en el README
3. Configura tus credenciales de API de forma segura
"""

def consultar_proveedor_api(nit):
    """
    PLACEHOLDER - Reemplaza con tu código de API
    
    Args:
        nit (str): NIT del proveedor sin dígito de verificación
        
    Returns:
        dict: Ver README para estructura completa esperada
    """
    return {
        'success': False,
        'error': '🔧 API no configurada. Completa la función en utils.py'
    }

def validar_nit(nit):
    """Validar formato básico del NIT"""
    if not nit:
        return False
    
    nit_clean = nit.replace(' ', '').replace('-', '')
    return nit_clean.isdigit() and len(nit_clean) >= 7
'''
        
        utils_path = self.proveedor_path / 'utils.py'
        if not utils_path.exists():
            utils_path.write_text(utils_content)
            print(f"✅ Creado: {utils_path}")
        
        # Archivo de configuración JavaScript
        js_config = '''/**
 * Configuración del módulo de proveedores
 * Personaliza estos valores según tu necesidad
 */

window.ProveedorConfig = {
    // URLs de la API (si usas endpoints personalizados)
    apiEndpoints: {
        consultarNit: '/proveedor/consultar-nit/',
        registrar: '/proveedor/registrar/',
        actualizar: '/proveedor/detalle/'
    },
    
    // Configuraciones de validación
    validation: {
        nitMinLength: 7,
        nitMaxLength: 15,
        nombreMinLength: 3
    },
    
    // Mensajes personalizados
    messages: {
        nitInvalido: 'NIT inválido. Solo números, 7-15 dígitos',
        nombreRequerido: 'El nombre es requerido',
        consultandoAPI: 'Consultando información del proveedor...'
    },
    
    // Configuración de UX
    ui: {
        showLoadingSpinner: true,
        autoFocusFirstField: true,
        validateOnType: true
    }
};
'''
        
        js_config_path = self.static_path / 'js' / 'config.js'
        if not js_config_path.exists():
            js_config_path.write_text(js_config)
            print(f"✅ Creado: {js_config_path}")
    
    def show_next_steps(self):
        """Mostrar pasos siguientes al usuario"""
        self.print_step(7, "Próximos pasos")
        
        print("""
🎯 SIGUIENTE: Completar la instalación

1. 📁 COPIAR ARCHIVOS DE LOS ARTIFACTS:
   - Copia models.py al directorio proveedor/
   - Copia views.py al directorio proveedor/  
   - Copia urls.py al directorio proveedor/
   - Copia admin.py al directorio proveedor/
   - Copia forms.py al directorio proveedor/ (opcional)
   - Copia validators.py al directorio proveedor/
   - Copia tests.py al directorio proveedor/
   
   - Copia todos los templates HTML a templates/proveedor/
   - Copia proveedor.js a static/proveedor/js/
   - Copia proveedor.css a static/proveedor/css/

2. 🔧 CONFIGURAR API:
   - Edita proveedor/utils.py
   - Agrega tu código de consulta de API
   - Configura credenciales de forma segura

3. 🗄️  CREAR BASE DE DATOS:
   cd app
   python manage.py makemigrations proveedor
   python manage.py migrate

4. 👤 CREAR SUPERUSUARIO (si no tienes):
   python manage.py createsuperuser

5. 🚀 PROBAR INSTALACIÓN:
   python manage.py runserver
   Ve a: http://localhost:8000/proveedor/

6. 🧪 EJECUTAR TESTS:
   python manage.py test proveedor

📚 DOCUMENTACIÓN COMPLETA:
   Ver README_MODULO_PROVEEDORES.md para detalles completos

⚠️  IMPORTANTE:
   - Revisa que todas las dependencias estén instaladas
   - Configura tu API antes de usar consultas por NIT
   - Personaliza estilos CSS según tu diseño
""")
    
    def run_installation(self):
        """Ejecutar proceso completo de instalación"""
        print("🚀 INSTALADOR DEL MÓDULO DE PROVEEDORES")
        print("="*60)
        
        try:
            # Verificar que es un proyecto Django
            if not self.check_django_project():
                print("❌ No es un proyecto Django válido")
                return False
            
            # Crear estructura de directorios
            self.create_directories()
            
            # Crear archivos de inicialización
            self.create_init_files()
            
            # Actualizar configuraciones
            self.update_settings()
            self.update_main_urls()
            
            # Crear archivos placeholder
            self.create_placeholder_files()
            
            # Mostrar próximos pasos
            self.show_next_steps()
            
            print("\n" + "="*60)
            print("✅ INSTALACIÓN BASE COMPLETADA")
            print("📋 Sigue los próximos pasos mostrados arriba")
            print("="*60)
            
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR durante la instalación: {str(e)}")
            print("   Revisa los mensajes anteriores para más detalles")
            return False

def main():
    """Función principal"""
    print("Instalador del Módulo de Proveedores v1.0")
    print("-" * 40)
    
    # Obtener ruta del proyecto
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = input("Ruta del proyecto Django (. para actual): ").strip() or "."
    
    # Confirmar instalación
    print(f"\n📂 Ruta del proyecto: {os.path.abspath(project_path)}")
    confirm = input("¿Continuar con la instalación? (s/N): ").lower()
    
    if confirm not in ['s', 'si', 'sí', 'yes', 'y']:
        print("❌ Instalación cancelada")
        return
    
    # Ejecutar instalación
    installer = ProveedorModuleInstaller(project_path)
    success = installer.run_installation()
    
    if success:
        print("\n🎉 ¡Módulo listo para configurar!")
    else:
        print("\n😞 Instalación incompleta. Revisa los errores.")

if __name__ == "__main__":
    main()