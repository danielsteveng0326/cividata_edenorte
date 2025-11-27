"""
Script para verificar la configuración del módulo PAA
Ejecutar desde la carpeta app: python test_paa_config.py
"""

import os
import sys
from pathlib import Path

print("=" * 60)
print("VERIFICACIÓN DE CONFIGURACIÓN PAA")
print("=" * 60)

# 1. Verificar variable de entorno
print("\n1. Variable de entorno GEMINI_API_KEY:")
api_key = os.environ.get('GEMINI_API_KEY')
if api_key:
    print(f"   ✅ Configurada: {api_key[:10]}...{api_key[-5:]}")
else:
    print("   ❌ NO CONFIGURADA")
    print("   Ejecute: $env:GEMINI_API_KEY='AIzaSyB5T7oGZkDoBa48qmP-C1c7uVfZszlwop8'")

# 2. Verificar plantilla
print("\n2. Plantilla PAA:")
plantilla_path = Path("paa/templates/paa/plantilla_paa.docx")
if plantilla_path.exists():
    print(f"   ✅ Encontrada: {plantilla_path.absolute()}")
    print(f"   Tamaño: {plantilla_path.stat().st_size} bytes")
else:
    print(f"   ❌ NO ENCONTRADA en: {plantilla_path.absolute()}")
    print("   Coloque su plantilla en esa ubicación")

# 3. Verificar módulos
print("\n3. Módulos Python:")
try:
    import google.generativeai as genai
    print("   ✅ google-generativeai instalado")
except ImportError:
    print("   ❌ google-generativeai NO instalado")
    print("   Ejecute: pip install google-generativeai==0.8.3")

try:
    from docx import Document
    print("   ✅ python-docx instalado")
except ImportError:
    print("   ❌ python-docx NO instalado")
    print("   Ejecute: pip install python-docx==1.2.0")

# 4. Probar conexión con Gemini (si está configurado)
if api_key:
    print("\n4. Probando conexión con Gemini:")
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Di 'OK'")
        print(f"   ✅ Conexión exitosa: {response.text[:50]}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

print("\n" + "=" * 60)
print("RESUMEN:")
print("=" * 60)

if api_key and plantilla_path.exists():
    print("✅ TODO CONFIGURADO CORRECTAMENTE")
    print("Puede usar el módulo PAA")
else:
    print("⚠️  CONFIGURACIÓN INCOMPLETA")
    if not api_key:
        print("   - Configure GEMINI_API_KEY")
    if not plantilla_path.exists():
        print("   - Coloque la plantilla PAA")

print("=" * 60)
