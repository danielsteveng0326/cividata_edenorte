#!/usr/bin/env python
"""
Script simple para crear un usuario administrador rápidamente
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
project_root = Path(__file__).parent
app_dir = project_root / 'app'  # Subdirectorio app
sys.path.append(str(app_dir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# Cambiar al directorio app antes de configurar Django
os.chdir(app_dir)
django.setup()

from django.contrib.auth.models import User

def create_admin():
    """Crear usuario administrador predeterminado"""
    
    # Configuración del usuario admin
    USERNAME = 'gerencia'
    EMAIL = 'edenorte@yarumal.gov.co'
    PASSWORD = 'NosUne.2025!'  # ¡CAMBIAR INMEDIATAMENTE!
    FIRST_NAME = 'Gerencia'
    LAST_NAME = 'Edenorte'
    
    try:
        # Eliminar si existe
        if User.objects.filter(username=USERNAME).exists():
            User.objects.filter(username=USERNAME).delete()
            print(f"🗑️  Usuario '{USERNAME}' existente eliminado")
        
        # Crear nuevo usuario
        user = User.objects.create_user(
            username=USERNAME,
            email=EMAIL,
            password=PASSWORD,
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            is_staff=True,
            is_superuser=True
        )
        
        print("✅ Usuario administrador creado exitosamente")
        print("=" * 50)
        print(f"👤 Usuario: {USERNAME}")
        print(f"🔑 Contraseña: {PASSWORD}")
        print(f"📧 Email: {EMAIL}")
        print("🔧 Permisos: Staff + Superusuario")
        print("=" * 50)
        print("⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_admin()