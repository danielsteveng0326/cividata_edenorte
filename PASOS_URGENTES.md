# 🚨 PASOS URGENTES - Solución Error 500

## El problema: Error 500 al generar certificado

**Causa:** La variable de entorno GEMINI_API_KEY no está configurada en la sesión actual del servidor.

---

## ✅ SOLUCIÓN RÁPIDA (3 pasos)

### Paso 1: Detener el servidor actual
Presione **Ctrl+C** en la terminal donde está corriendo el servidor

### Paso 2: Configurar la variable de entorno

En la **misma terminal** donde va a ejecutar el servidor, ejecute:

```powershell
$env:GEMINI_API_KEY="AIzaSyDHfLmtrYnDgkTWb43DXFftk2XMZGy_4wY"
```

**O use el script:**
```powershell
cd app
.\configurar_env_temporal.ps1
```

### Paso 3: Iniciar el servidor

```powershell
python manage.py runserver
```

---

## 🔍 VERIFICAR CONFIGURACIÓN

Antes de iniciar el servidor, ejecute el script de verificación:

```powershell
cd app
python test_paa_config.py
```

Esto le dirá exactamente qué falta configurar.

---

## 📋 CHECKLIST

Ejecute estos comandos en orden:

```powershell
# 1. Ir a la carpeta app
cd "C:\Users\danie\OneDrive - SENA\Documentos\Dev\cividata_edenorte\app"

# 2. Activar entorno virtual (si no está activado)
..\venv\Scripts\Activate.ps1

# 3. Configurar variable de entorno
$env:GEMINI_API_KEY="AIzaSyDHfLmtrYnDgkTWb43DXFftk2XMZGy_4wY"

# 4. Verificar que esté configurada
echo $env:GEMINI_API_KEY

# 5. Verificar configuración completa
python test_paa_config.py

# 6. Iniciar servidor
python manage.py runserver
```

---

## ⚠️ IMPORTANTE

La variable `$env:GEMINI_API_KEY` es **temporal** y solo funciona en esa sesión de terminal.

Si cierra la terminal, debe configurarla nuevamente.

---

## 🎯 VERIFICAR QUE FUNCIONA

1. Abra: http://localhost:8000/paa/
2. Cargue un archivo .docx
3. Haga clic en "Generar Certificado PAA"
4. Si ve el error 500, revise la terminal del servidor para ver el error detallado

---

## 📝 NOTAS

- El click en la zona de carga ya está corregido (usa `<label>`)
- El servidor mostrará el error detallado en la consola
- Use `test_paa_config.py` para diagnosticar problemas

---

## 🆘 SI PERSISTE EL ERROR

Revise la terminal del servidor. Ahora mostrará:
```
ERROR DETALLADO:
[stack trace completo del error]
```

Esto le dirá exactamente qué está fallando:
- ❌ API key no configurada
- ❌ Plantilla no encontrada  
- ❌ Error de Gemini
- ❌ Otro error

---

**¡Ejecute los comandos del CHECKLIST en orden y el error se solucionará!**
