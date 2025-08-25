#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de instalación para Windows - Módulo de Proveedores
Versión corregida para manejo de codificación en Windows
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
            print(f"Creado: {directory}")
    
    def create_init_files(self):
        """Crear archivos __init__.py necesarios"""
        self.print_step(2, "Creando archivos de inicializacion")
        
        init_files = [
            self.proveedor_path / '__init__.py',
            self.proveedor_path / 'migrations' / '__init__.py'
        ]
        
        for init_file in init_files:
            if not init_file.exists():
                with open(init_file, 'w', encoding='utf-8') as f:
                    f.write('# Auto-generated __init__.py\n')
                print(f"Creado: {init_file}")
    
    def check_django_project(self):
        """Verificar que es un proyecto Django válido"""
        self.print_step(3, "Verificando proyecto Django")
        
        manage_py = self.app_path / 'manage.py'
        settings_py = self.app_path / 'app' / 'settings.py'
        
        if not manage_py.exists():
            print("ERROR: No se encontro manage.py")
            return False
        
        if not settings_py.exists():
            print("ERROR: No se encontro settings.py")
            return False
        
        print("Proyecto Django valido detectado")
        return True
    
    def update_settings(self):
        """Actualizar settings.py para incluir la app proveedor"""
        self.print_step(4, "Actualizando settings.py")
        
        settings_path = self.app_path / 'app' / 'settings.py'
        
        if not settings_path.exists():
            print("ERROR: No se encontro settings.py")
            return False
        
        with open(settings_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si ya está agregado
        if "'proveedor'" in content:
            print("La app 'proveedor' ya esta en INSTALLED_APPS")
            return True
        
        # Buscar INSTALLED_APPS y agregar proveedor
        pattern = r'(INSTALLED_APPS\s*=\s*\[.*?)(])'
        
        def replace_installed_apps(match):
            apps_content = match.group(1)
            closing_bracket = match.group(2)
            
            if not apps_content.strip().endswith(','):
                apps_content += ','
            
            return f"{apps_content}\n    'proveedor',{closing_bracket}"
        
        updated_content = re.sub(pattern, replace_installed_apps, content, flags=re.DOTALL)
        
        if updated_content != content:
            # Hacer backup
            backup_path = settings_path.with_suffix('.py.backup')
            settings_path.rename(backup_path)
            print(f"Backup creado: {backup_path}")
            
            # Escribir archivo actualizado
            with open(settings_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print("settings.py actualizado con 'proveedor' app")
        else:
            print("ADVERTENCIA: No se pudo actualizar settings.py automaticamente")
            print("Por favor agrega manualmente 'proveedor' a INSTALLED_APPS")
        
        return True
    
    def update_main_urls(self):
        """Actualizar urls.py principal para incluir rutas de proveedor"""
        self.print_step(5, "Actualizando URLs principales")
        
        urls_path = self.app_path / 'app' / 'urls.py'
        
        if not urls_path.exists():
            print("ERROR: No se encontro urls.py principal")
            return False
        
        with open(urls_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si ya está agregado
        if "proveedor.urls" in content:
            print("Las URLs de proveedor ya estan configuradas")
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
            new_pattern = "\n    path('proveedor/', include('proveedor.urls')),"
            return f"{patterns_content}{new_pattern}{closing_bracket}"
        
        updated_content = re.sub(pattern, replace_urlpatterns, content, flags=re.DOTALL)
        
        if updated_content != content:
            backup_path = urls_path.with_suffix('.py.backup')
            settings_path.rename(backup_path)
            print(f"Backup creado: {backup_path}")
            
            with open(urls_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print("urls.py actualizado con rutas de proveedor")
        else:
            print("ADVERTENCIA: No se pudo actualizar urls.py automaticamente")
            print("Por favor agrega manualmente: path('proveedor/', include('proveedor.urls'))")
        
        return True
    
    def create_placeholder_files(self):
        """Crear archivos placeholder para que el usuario complete"""
        self.print_step(6, "Creando archivos placeholder")
        
        # Archivo utils.py con placeholder para API (SIN emojis para Windows)
        utils_content = '''"""
Funciones para consulta de proveedores a traves de API externa

INSTRUCCIONES IMPORTANTES:
1. Reemplaza la funcion consultar_proveedor_api() con tu codigo de API real
2. La funcion debe retornar el formato especificado en el README
3. Configura tus credenciales de API de forma segura
"""

def consultar_proveedor_api(nit):
    """
    PLACEHOLDER - Reemplaza con tu codigo de API
    
    Args:
        nit (str): NIT del proveedor sin digito de verificacion
        
    Returns:
        dict: Ver README para estructura completa esperada
    """
    return {
        'success': False,
        'error': 'API no configurada. Completa la funcion en utils.py'
    }

def validar_nit(nit):
    """Validar formato basico del NIT"""
    if not nit:
        return False
    
    nit_clean = nit.replace(' ', '').replace('-', '')
    return nit_clean.isdigit() and len(nit_clean) >= 7
'''
        
        utils_path = self.proveedor_path / 'utils.py'
        if not utils_path.exists():
            with open(utils_path, 'w', encoding='utf-8') as f:
                f.write(utils_content)
            print(f"Creado: {utils_path}")
        
        # Archivo de configuración JavaScript (SIN caracteres especiales)
        js_config = '''/**
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
'''
        
        js_config_path = self.static_path / 'js' / 'config.js'
        if not js_config_path.exists():
            with open(js_config_path, 'w', encoding='utf-8') as f:
                f.write(js_config)
            print(f"Creado: {js_config_path}")
    
    def show_next_steps(self):
        """Mostrar pasos siguientes al usuario"""
        self.print_step(7, "Proximos pasos")
        
        print("""
SIGUIENTE: Completar la instalacion

1. COPIAR ARCHIVOS DE LOS ARTIFACTS:
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

2. CONFIGURAR API:
   - Edita proveedor/utils.py
   - Agrega tu codigo de consulta de API
   - Configura credenciales de forma segura

3. CREAR BASE DE DATOS:
   cd app
   python manage.py makemigrations proveedor
   python manage.py migrate

4. CREAR SUPERUSUARIO (si no tienes):
   python manage.py createsuperuser

5. PROBAR INSTALACION:
   python manage.py runserver
   Ve a: http://localhost:8000/proveedor/

6. EJECUTAR TESTS:
   python manage.py test proveedor

DOCUMENTACION COMPLETA:
   Ver README_MODULO_PROVEEDORES.md para detalles completos

IMPORTANTE:
   - Revisa que todas las dependencias esten instaladas
   - Configura tu API antes de usar consultas por NIT
   - Personaliza estilos CSS segun tu diseno
""")
    
    def run_installation(self):
        """Ejecutar proceso completo de instalación"""
        print("INSTALADOR DEL MODULO DE PROVEEDORES")
        print("="*60)
        
        try:
            if not self.check_django_project():
                print("ERROR: No es un proyecto Django valido")
                return False
            
            self.create_directories()
            self.create_init_files()
            self.update_settings()
            self.update_main_urls()
            self.create_placeholder_files()
            self.show_next_steps()
            
            print("\n" + "="*60)
            print("INSTALACION BASE COMPLETADA")
            print("Sigue los proximos pasos mostrados arriba")
            print("="*60)
            
            return True
            
        except Exception as e:
            print(f"\nERROR durante la instalacion: {str(e)}")
            print("Revisa los mensajes anteriores para mas detalles")
            import traceback
            print("\nDetalle del error:")
            traceback.print_exc()
            return False

def main():
    """Función principal"""
    print("Instalador del Modulo de Proveedores v1.0 (Windows)")
    print("-" * 50)
    
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = input("Ruta del proyecto Django (. para actual): ").strip() or "."
    
    print(f"\nRuta del proyecto: {os.path.abspath(project_path)}")
    confirm = input("Continuar con la instalacion? (s/N): ").lower()
    
    if confirm not in ['s', 'si', 'yes', 'y']:
        print("Instalacion cancelada")
        return
    
    installer = ProveedorModuleInstaller(project_path)
    success = installer.run_installation()
    
    if success:
        print("\nModulo listo para configurar!")
    else:
        print("\nInstalacion incompleta. Revisa los errores.")
    
    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()