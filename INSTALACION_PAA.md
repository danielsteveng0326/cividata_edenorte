# Instalación y Configuración del Módulo PAA

## 📋 Resumen

El módulo PAA (Plan Anual de Adquisiciones) permite generar automáticamente certificados PAA a partir de un Estudio Previo en formato Word (.docx), utilizando Gemini 2.5 Flash para extraer la información necesaria.

## 🚀 Pasos de Instalación

### 1. Instalar Dependencias

```bash
cd app
pip install -r ../requirements.txt
```

O específicamente:
```bash
pip install google-generativeai==0.8.3
pip install python-docx==1.2.0
```

### 2. Configurar Variable de Entorno

#### Opción A: Archivo .env (Desarrollo Local)

Cree o edite el archivo `.env` en la raíz del proyecto:

```env
GEMINI_API_KEY=your-gemini-api-key-here
```

#### Opción B: Variables de Sistema (Windows)

```powershell
# PowerShell
$env:GEMINI_API_KEY="your-gemini-api-key-here"

# O permanentemente
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'your-gemini-api-key-here', 'User')
```

#### Opción C: Railway (Producción)

1. Vaya a su proyecto en Railway
2. Navegue a **Variables**
3. Agregue una nueva variable:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: `your-gemini-api-key-here`

### 3. Obtener API Key de Gemini

1. Visite: https://makersuite.google.com/app/apikey
2. Inicie sesión con su cuenta de Google
3. Haga clic en **"Create API Key"**
4. Copie la API key generada
5. Úsela en el paso anterior

### 4. Crear la Plantilla PAA

#### Opción A: Usar el Script Automático

```bash
cd app/paa
python crear_plantilla_ejemplo.py
```

Esto creará una plantilla básica en `app/paa/templates/paa/plantilla_paa.docx`

#### Opción B: Crear Manualmente

1. Cree un documento Word con el formato oficial de EDENORTE
2. Incluya los siguientes placeholders exactamente como se muestran:
   - `{{w_gen}}` - Género (EL o LA)
   - `{{w_cargo}}` - Cargo del usuario
   - `{{w_anno}}` - Año actual
   - `{{w_codigos}}` - Códigos UNSPSC
   - `{{w_objeto}}` - Objeto del contrato
   - `{{w_valor}}` - Valor del contrato
   - `{{w_plazo}}` - Plazo del contrato
   - `{{w_fecha}}` - Fecha en letras

3. Guarde el archivo como: `app/paa/templates/paa/plantilla_paa.docx`

### 5. Aplicar Migraciones (si es necesario)

```bash
cd app
python manage.py makemigrations
python manage.py migrate
```

### 6. Ejecutar el Servidor

```bash
python manage.py runserver
```

## ✅ Verificación

1. Acceda a: http://localhost:8000/login/
2. Inicie sesión
3. Navegue a: **Asistente Contratación > PAA**
4. Debería ver la interfaz de carga de documentos

## 📁 Estructura de Archivos Creados

```
app/
├── paa/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── README.md
│   ├── crear_plantilla_ejemplo.py
│   └── templates/
│       └── paa/
│           ├── index.html
│           ├── plantilla_paa.docx  (debe crearse)
│           └── README_PLANTILLA.md
├── app/
│   ├── settings.py  (modificado - agregada app 'paa')
│   └── urls.py      (modificado - agregada ruta 'paa/')
└── templates/
    └── navbar.html  (modificado - agregado enlace PAA)
```

## 🔧 Configuración Adicional

### settings.py

Se agregó:
```python
INSTALLED_APPS = [
    # ...
    'paa',
]

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
```

### urls.py

Se agregó:
```python
urlpatterns = [
    # ...
    path('paa/', include('paa.urls')),
]
```

### navbar.html

Se agregó el menú:
```html
<li class="nav-item">
  <a href="{% url 'paa:index' %}" class="nav-link">
    <i class="far fa-circle nav-icon"></i>
    <p>PAA</p>
  </a>
</li>
```

## 🧪 Prueba del Sistema

1. Prepare un archivo Word con un Estudio Previo
2. Acceda al módulo PAA
3. Cargue el archivo
4. Complete género y cargo
5. Haga clic en "Generar Certificado PAA"
6. El sistema debería:
   - Mostrar un loading
   - Procesar el documento con Gemini
   - Descargar automáticamente el certificado generado

## ⚠️ Solución de Problemas

### Error: "No se ha configurado la variable de entorno GEMINI_API_KEY"

**Solución:**
- Verifique que la variable `GEMINI_API_KEY` esté configurada
- Reinicie el servidor Django después de configurar la variable
- En desarrollo, use un archivo `.env` o configure la variable de sistema

### Error: "No se encontró la plantilla"

**Solución:**
- Verifique que existe el archivo `plantilla_paa.docx`
- La ruta debe ser exactamente: `app/paa/templates/paa/plantilla_paa.docx`
- Ejecute el script `crear_plantilla_ejemplo.py` para crear una plantilla básica

### Error: "Module 'google.generativeai' not found"

**Solución:**
```bash
pip install google-generativeai==0.8.3
```

### El certificado no se genera correctamente

**Solución:**
- Verifique que el Estudio Previo contenga la información necesaria
- Revise los logs del servidor para ver el error específico
- Asegúrese de que la API key de Gemini sea válida y tenga cuota disponible

## 📊 Uso de la API de Gemini

El sistema usa el modelo `gemini-2.0-flash-exp` que:
- Es gratuito con límites generosos
- Tiene alta precisión en extracción de texto
- Soporta documentos largos
- Responde en segundos

**Límites gratuitos de Gemini:**
- 15 solicitudes por minuto
- 1 millón de tokens por minuto
- 1,500 solicitudes por día

## 🔐 Seguridad

- La API key se almacena en variables de entorno (nunca en el código)
- Los archivos cargados se procesan en memoria (no se guardan en disco)
- El sistema requiere autenticación (login)
- Los certificados se generan bajo demanda

## 📝 Notas Adicionales

- El sistema convierte automáticamente todo el texto a MAYÚSCULAS
- La fecha se genera en español con el formato: "el seis (6) días del mes de octubre de 2025"
- Los códigos UNSPSC se separan por coma
- La plantilla PAA NO se modifica, solo se reemplazan los placeholders

## 🆘 Soporte

Para problemas o preguntas:
1. Revise los logs del servidor Django
2. Verifique la consola del navegador (F12)
3. Consulte el archivo `app/paa/README.md`
4. Revise la documentación de Gemini: https://ai.google.dev/docs

## 📚 Recursos

- **Gemini API**: https://ai.google.dev/
- **python-docx**: https://python-docx.readthedocs.io/
- **Django**: https://docs.djangoproject.com/
