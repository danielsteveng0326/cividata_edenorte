#!/usr/bin/env python3
"""
Script de diagnóstico para el módulo de proveedores
Ejecutar desde la carpeta app/: python debug_proveedor.py
"""

import os
import sys
from pathlib import Path

def print_status(message, status):
    icon = "OK" if status else "ERROR"
    print(f"[{icon}] {message}")

def check_file_exists(filepath):
    exists = Path(filepath).exists()
    print_status(f"Archivo {filepath}", exists)
    return exists

def check_directory_structure():
    print("VERIFICANDO ESTRUCTURA DE ARCHIVOS")
    print("-" * 50)
    
    files_to_check = [
        "proveedor/__init__.py",
        "proveedor/models.py", 
        "proveedor/views.py",
        "proveedor/urls.py",
        "proveedor/apps.py",
        "proveedor/migrations/__init__.py",
        "templates/proveedor/index.html"
    ]
    
    all_exist = True
    for file in files_to_check:
        if not check_file_exists(file):
            all_exist = False
    
    return all_exist

def check_settings_configuration():
    print("\nVERIFICANDO CONFIGURACIÓN")
    print("-" * 50)
    
    try:
        settings_file = Path("app/settings.py")
        if settings_file.exists():
            content = settings_file.read_text()
            has_proveedor = "'proveedor'" in content or '"proveedor"' in content
            print_status("'proveedor' en INSTALLED_APPS", has_proveedor)
            return has_proveedor
        else:
            print_status("Archivo settings.py encontrado", False)
            return False
    except Exception as e:
        print(f"[ERROR] Error leyendo settings.py: {e}")
        return False

def check_main_urls():
    print("\nVERIFICANDO URLs PRINCIPALES")
    print("-" * 50)
    
    try:
        urls_file = Path("app/urls.py")
        if urls_file.exists():
            content = urls_file.read_text()
            has_proveedor_url = "proveedor" in content and "include" in content
            print_status("Ruta 'proveedor/' en URLs principales", has_proveedor_url)
            return has_proveedor_url
        else:
            print_status("Archivo urls.py encontrado", False)
            return False
    except Exception as e:
        print(f"[ERROR] Error leyendo urls.py: {e}")
        return False

def check_django_setup():
    print("\nVERIFICANDO DJANGO")
    print("-" * 50)
    
    try:
        import django
        print_status(f"Django instalado (versión {django.get_version()})", True)
        
        manage_exists = Path("manage.py").exists()
        print_status("manage.py encontrado", manage_exists)
        
        return True
    except ImportError:
        print_status("Django instalado", False)
        return False

def generate_minimal_files():
    print("\nGENERANDO ARCHIVOS MÍNIMOS PARA DEBUG")
    print("-" * 50)
    
    os.makedirs("proveedor", exist_ok=True)
    os.makedirs("proveedor/migrations", exist_ok=True)
    os.makedirs("templates/proveedor", exist_ok=True)
    
    Path("proveedor/__init__.py").write_text("# Proveedor module\n")
    print_status("Creado proveedor/__init__.py", True)
    
    Path("proveedor/migrations/__init__.py").write_text("# Migrations\n")
    print_status("Creado proveedor/migrations/__init__.py", True)
    
    apps_content = '''from django.apps import AppConfig

class ProveedorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'proveedor'
'''
    Path("proveedor/apps.py").write_text(apps_content)
    print_status("Creado proveedor/apps.py", True)
    
    print("\nArchivos mínimos generados. Ahora copia los archivos de los artifacts:")
    print("1. proveedor/models.py")
    print("2. proveedor/views.py") 
    print("3. proveedor/urls.py")
    print("4. templates/proveedor/index.html")

def show_next_steps():
    print("\nPRÓXIMOS PASOS PARA SOLUCIONAR")
    print("-" * 50)
    print("1. Si faltan archivos: copiar los artifacts correspondientes")
    print("2. Agregar 'proveedor' a INSTALLED_APPS en settings.py")
    print("3. Agregar path('proveedor/', include('proveedor.urls')) a urls.py") 
    print("4. Ejecutar: python manage.py makemigrations proveedor")
    print("5. Ejecutar: python manage.py migrate")
    print("6. Reiniciar servidor: python manage.py runserver")

def main():
    print("DIAGNÓSTICO MÓDULO PROVEEDORES")
    print("=" * 50)
    
    if not Path("manage.py").exists():
        print("[ERROR] No se encontró manage.py")
        print("   Ejecuta este script desde la carpeta app/ de tu proyecto Django")
        return
    
    structure_ok = check_directory_structure()
    django_ok = check_django_setup()
    settings_ok = check_settings_configuration()
    urls_ok = check_main_urls()
    
    print(f"\nRESUMEN:")
    print(f"- Estructura archivos: {'OK' if structure_ok else 'ERROR'}")
    print(f"- Django configurado: {'OK' if django_ok else 'ERROR'}")
    print(f"- Settings configurado: {'OK' if settings_ok else 'ERROR'}")
    print(f"- URLs configurado: {'OK' if urls_ok else 'ERROR'}")
    
    if not structure_ok:
        generate_minimal_files()
    
    show_next_steps()
    
    print(f"\nDEBUG DETALLADO:")
    print("1. Comparte el error específico que ves en el navegador")
    print("2. Comparte los logs de la consola de Django")
    print("3. Ejecuta: python manage.py check")

if __name__ == "__main__":
    main()
