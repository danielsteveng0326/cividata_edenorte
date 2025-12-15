# ✅ Módulo PAA - Pasos Finales de Configuración

## 🎉 Estado Actual

El módulo PAA ha sido **completamente implementado** con las siguientes características:

### ✅ Archivos Creados

1. **Aplicación Django PAA** (`app/paa/`)
   - `views.py` - Lógica de procesamiento con Gemini 2.5 Flash
   - `urls.py` - Rutas de la aplicación
   - `templates/paa/index.html` - Interfaz de usuario moderna
   - `crear_plantilla_ejemplo.py` - Script para generar plantilla

2. **Configuración del Sistema**
   - `app/app/settings.py` - App agregada a INSTALLED_APPS
   - `app/app/urls.py` - Ruta `/paa/` configurada
   - `app/templates/navbar.html` - Menú "Asistente Contratación > PAA" agregado
   - `requirements.txt` - Dependencia `google-generativeai` agregada

3. **Documentación**
   - `INSTALACION_PAA.md` - Guía completa de instalación
   - `app/paa/README.md` - Documentación del módulo
   - `app/paa/templates/paa/README_PLANTILLA.md` - Guía de la plantilla
   - `.env.example` - Ejemplo de variables de entorno

## 🚀 Pasos Finales (DEBE EJECUTAR)

### 1. Instalar Dependencias

Abra una terminal en la carpeta del proyecto y ejecute:

```bash
# Activar entorno virtual (si está usando uno)
# En Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install google-generativeai==0.8.3
pip install python-docx==1.2.0
```

O instalar todo desde requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Configurar API Key de Gemini

#### Paso 2.1: Obtener API Key

1. Visite: https://makersuite.google.com/app/apikey
2. Inicie sesión con su cuenta de Google
3. Haga clic en **"Create API Key"**
4. Copie la API key generada

#### Paso 2.2: Configurar Variable de Entorno

**Opción A - Desarrollo Local (Recomendado):**

Cree un archivo `.env` en la raíz del proyecto:

```env
GEMINI_API_KEY=AIzaSy...  # Pegue su API key aquí
```

**Opción B - Variable de Sistema (Windows):**

```powershell
# Temporal (solo para la sesión actual)
$env:GEMINI_API_KEY="AIzaSy..."

# Permanente
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'AIzaSy...', 'User')
```

**Opción C - Railway (Producción):**

1. Vaya a su proyecto en Railway
2. Navegue a **Variables**
3. Agregue: `GEMINI_API_KEY` = `AIzaSy...`

### 3. Crear la Plantilla PAA

Ejecute el script para crear una plantilla de ejemplo:

```bash
cd app\paa
python crear_plantilla_ejemplo.py
```

Esto creará el archivo: `app/paa/templates/paa/plantilla_paa.docx`

**⚠️ IMPORTANTE:** Esta es una plantilla de ejemplo. Debe reemplazarla con el formato oficial de EDENORTE manteniendo los placeholders:

- `{{w_gen}}`
- `{{w_cargo}}`
- `{{w_anno}}`
- `{{w_codigos}}`
- `{{w_objeto}}`
- `{{w_valor}}`
- `{{w_plazo}}`
- `{{w_fecha}}`

### 4. Aplicar Migraciones (si es necesario)

```bash
cd app
python manage.py makemigrations
python manage.py migrate
```

### 5. Ejecutar el Servidor

```bash
cd app
python manage.py runserver
```

### 6. Probar el Módulo

1. Acceda a: http://localhost:8000/login/
2. Inicie sesión
3. En el menú lateral, vaya a: **Asistente Contratación > PAA**
4. Cargue un archivo Word con un Estudio Previo
5. Complete género y cargo
6. Haga clic en "Generar Certificado PAA"

## 📋 Checklist de Verificación

Marque cada paso completado:

- [ ] Dependencias instaladas (`google-generativeai` y `python-docx`)
- [ ] API Key de Gemini obtenida
- [ ] Variable de entorno `GEMINI_API_KEY` configurada
- [ ] Plantilla PAA creada en `app/paa/templates/paa/plantilla_paa.docx`
- [ ] Servidor Django ejecutándose sin errores
- [ ] Menú "Asistente Contratación > PAA" visible en el navbar
- [ ] Página PAA carga correctamente
- [ ] Prueba de generación de certificado exitosa

## 🔧 Solución de Problemas Comunes

### Error: "No module named 'google.generativeai'"

**Solución:**
```bash
pip install google-generativeai==0.8.3
```

### Error: "No module named 'docx'"

**Solución:**
```bash
pip install python-docx==1.2.0
```

### Error: "No se ha configurado la variable de entorno GEMINI_API_KEY"

**Solución:**
1. Verifique que la variable esté configurada
2. Reinicie el servidor Django
3. Si usa `.env`, asegúrese de tener `python-decouple` instalado

### Error: "No se encontró la plantilla"

**Solución:**
```bash
cd app\paa
python crear_plantilla_ejemplo.py
```

### La página PAA no carga

**Solución:**
1. Verifique que la app 'paa' esté en INSTALLED_APPS
2. Ejecute: `python manage.py migrate`
3. Reinicie el servidor

## 📊 Características Implementadas

### ✅ Interfaz de Usuario
- Diseño moderno y responsivo
- Drag & drop para cargar archivos
- Validación de archivos .docx
- Indicadores de progreso
- Notificaciones con SweetAlert2

### ✅ Procesamiento con IA
- Usa Gemini 2.5 Flash (`gemini-2.0-flash-exp`)
- Extracción automática de:
  - Objeto del contrato
  - Valor estimado
  - Plazo o duración
  - Códigos UNSPSC
- Limpieza y normalización de texto
- Conversión a MAYÚSCULAS

### ✅ Generación de Documentos
- Reemplazo de placeholders en plantilla
- Preservación del formato original
- Generación de fecha en español
- Descarga automática del certificado

### ✅ Seguridad
- Autenticación requerida
- Validación de archivos
- API key en variables de entorno
- Procesamiento en memoria (no se guardan archivos)

## 📚 Documentación Adicional

Para más información, consulte:

- `INSTALACION_PAA.md` - Guía detallada de instalación
- `app/paa/README.md` - Documentación técnica del módulo
- `app/paa/templates/paa/README_PLANTILLA.md` - Guía de la plantilla

## 🎯 Próximos Pasos

Una vez completados los pasos finales:

1. **Personalizar la plantilla** con el formato oficial de EDENORTE
2. **Probar con documentos reales** de Estudios Previos
3. **Ajustar el prompt de Gemini** si es necesario para mejorar la extracción
4. **Configurar en producción** (Railway) con la variable GEMINI_API_KEY

## 🆘 Soporte

Si encuentra problemas:

1. Revise los logs del servidor Django
2. Verifique la consola del navegador (F12)
3. Consulte la documentación en los archivos README
4. Verifique que todas las dependencias estén instaladas

---

**¡El módulo PAA está listo para usar! Solo faltan los pasos finales de configuración.**
