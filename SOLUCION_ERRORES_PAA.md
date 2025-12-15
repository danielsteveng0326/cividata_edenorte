# 🔧 Solución de Errores PAA

## ✅ Errores Corregidos

### 1. ❌ Click en zona de carga no funciona
**SOLUCIONADO** - Se agregó `e.preventDefault()` al evento click

### 2. ❌ Error 500 al generar certificado
**Causas posibles:**
- Variable de entorno GEMINI_API_KEY no configurada
- Plantilla PAA no existe en la ubicación correcta

---

## 🚀 Pasos para Solucionar

### Paso 1: Configurar Variable de Entorno GEMINI_API_KEY

**Opción A - Usar el Script PowerShell (Recomendado):**

1. Abra PowerShell como **Administrador**
2. Navegue a la carpeta del proyecto:
   ```powershell
   cd "C:\Users\danie\OneDrive - SENA\Documentos\Dev\cividata_edenorte"
   ```
3. Ejecute el script:
   ```powershell
   .\configurar_gemini.ps1
   ```
4. **IMPORTANTE:** Cierre y vuelva a abrir la terminal

**Opción B - Configurar Manualmente:**

En PowerShell:
```powershell
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'AIzaSyDHfLmtrYnDgkTWb43DXFftk2XMZGy_4wY', 'User')
```

**Opción C - Configurar para la Sesión Actual (Temporal):**

```powershell
$env:GEMINI_API_KEY="AIzaSyDHfLmtrYnDgkTWb43DXFftk2XMZGy_4wY"
```

### Paso 2: Verificar que la Variable Esté Configurada

En una **nueva terminal** PowerShell:
```powershell
echo $env:GEMINI_API_KEY
```

Debería mostrar: `AIzaSyDHfLmtrYnDgkTWb43DXFftk2XMZGy_4wY`

### Paso 3: Colocar la Plantilla PAA

Asegúrese de que su archivo `plantilla_paa.docx` esté en:
```
C:\Users\danie\OneDrive - SENA\Documentos\Dev\cividata_edenorte\app\paa\templates\paa\plantilla_paa.docx
```

**Verificar la ruta:**
```powershell
Test-Path "C:\Users\danie\OneDrive - SENA\Documentos\Dev\cividata_edenorte\app\paa\templates\paa\plantilla_paa.docx"
```

Debe devolver `True`

### Paso 4: Reiniciar el Servidor Django

1. Detenga el servidor actual (Ctrl+C)
2. En una **nueva terminal** con el entorno virtual activado:
   ```powershell
   cd "C:\Users\danie\OneDrive - SENA\Documentos\Dev\cividata_edenorte\app"
   .\venv\Scripts\Activate.ps1
   python manage.py runserver
   ```

### Paso 5: Probar Nuevamente

1. Acceda a: http://localhost:8000/paa/
2. Haga clic en la zona de carga (ahora debería abrir el explorador)
3. Seleccione un archivo .docx con el Estudio Previo
4. Haga clic en "Generar Certificado PAA"

---

## 🔍 Diagnóstico de Errores

### Si sigue mostrando error 500:

**1. Verificar logs del servidor**

Los logs mostrarán el error específico. Busque líneas que digan:
- `Error al procesar con Gemini: ...`
- `No se encontró la plantilla PAA...`
- `No se ha configurado la variable de entorno GEMINI_API_KEY...`

**2. Verificar que Gemini esté funcionando**

Pruebe la API key manualmente:
```python
import google.generativeai as genai
import os

api_key = os.environ.get('GEMINI_API_KEY')
print(f"API Key: {api_key[:10]}..." if api_key else "No configurada")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash-exp')
response = model.generate_content("Hola")
print(response.text)
```

**3. Verificar que la plantilla existe**

```python
from pathlib import Path
plantilla = Path("app/paa/templates/paa/plantilla_paa.docx")
print(f"Plantilla existe: {plantilla.exists()}")
print(f"Ruta completa: {plantilla.absolute()}")
```

---

## 📋 Checklist de Verificación

- [ ] Variable GEMINI_API_KEY configurada
- [ ] Terminal reiniciada después de configurar la variable
- [ ] Variable verificada con `echo $env:GEMINI_API_KEY`
- [ ] Plantilla `plantilla_paa.docx` en la ubicación correcta
- [ ] Servidor Django reiniciado
- [ ] Click en zona de carga funciona (abre explorador)
- [ ] Archivo se puede arrastrar y soltar
- [ ] Certificado se genera sin errores

---

## 🆘 Si Persisten los Errores

### Error: "No se ha configurado la variable de entorno GEMINI_API_KEY"

**Solución:**
1. Cierre TODAS las terminales y ventanas de VS Code
2. Abra una nueva terminal PowerShell
3. Configure la variable nuevamente
4. Verifique con `echo $env:GEMINI_API_KEY`
5. Inicie el servidor

### Error: "No se encontró la plantilla PAA"

**Solución:**
1. Verifique la ruta exacta del archivo
2. Asegúrese de que el nombre sea exactamente `plantilla_paa.docx`
3. Verifique que esté en la carpeta correcta

### Error: "Error al procesar con Gemini"

**Posibles causas:**
- API key inválida o expirada
- Límite de cuota excedido
- Problema de conexión a internet

**Solución:**
1. Verifique que la API key sea válida en https://makersuite.google.com/app/apikey
2. Revise los límites de uso de Gemini
3. Verifique su conexión a internet

---

## 📞 Comandos Útiles

**Ver variable de entorno:**
```powershell
echo $env:GEMINI_API_KEY
```

**Configurar variable (temporal):**
```powershell
$env:GEMINI_API_KEY="AIzaSyDHfLmtrYnDgkTWb43DXFftk2XMZGy_4wY"
```

**Verificar plantilla:**
```powershell
Test-Path "app\paa\templates\paa\plantilla_paa.docx"
```

**Iniciar servidor:**
```powershell
cd app
python manage.py runserver
```

---

**¡Los errores han sido corregidos en el código! Solo falta configurar la variable de entorno.**
