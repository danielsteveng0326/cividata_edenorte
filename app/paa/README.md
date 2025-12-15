# Módulo PAA - Plan Anual de Adquisiciones

## Descripción

Módulo para generar automáticamente Certificados del Plan Anual de Adquisiciones (PAA) a partir de un Estudio Previo en formato Word (.docx).

## Funcionalidades

- **Carga de Estudio Previo**: El usuario carga un archivo .docx con el estudio previo
- **Extracción Automática**: Usa Gemini 2.5 Flash para extraer:
  - Objeto del contrato
  - Valor estimado
  - Plazo o duración
  - Códigos UNSPSC
- **Generación de Certificado**: Crea un documento en el formato oficial del PAA
- **Exportación Múltiple**: Permite exportar el certificado en dos formatos:
  - **Word (.docx)**: Documento editable
  - **PDF (.pdf)**: Documento listo para imprimir
- **Descarga Automática**: El usuario descarga el certificado generado en el formato seleccionado

## Configuración

### 1. Variables de Entorno

Debe configurar la variable de entorno `GEMINI_API_KEY` con su API key de Google Gemini:

```bash
# En .env o en las variables de entorno del sistema
GEMINI_API_KEY=your-gemini-api-key-here
```

### 2. Obtener API Key de Gemini

1. Visite [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicie sesión con su cuenta de Google
3. Cree una nueva API key
4. Copie la API key y agréguela a sus variables de entorno

### 3. Plantilla PAA

Debe crear un archivo Word llamado `plantilla_paa.docx` en la carpeta:
```
app/paa/templates/paa/plantilla_paa.docx
```

La plantilla debe contener los siguientes placeholders:

- `{{w_gen}}` - Género (EL o LA)
- `{{w_cargo}}` - Cargo del usuario
- `{{w_anno}}` - Año actual
- `{{w_codigos}}` - Códigos UNSPSC
- `{{w_objeto}}` - Objeto del contrato
- `{{w_valor}}` - Valor del contrato
- `{{w_plazo}}` - Plazo del contrato
- `{{w_fecha}}` - Fecha en letras

Ver `README_PLANTILLA.md` para más detalles sobre la plantilla.

## Uso

1. Acceda al módulo desde el menú: **Asistente Contratación > PAA**
2. Cargue el archivo Word con el Estudio Previo (arrastrando o haciendo clic)
3. Seleccione el formato de salida deseado:
   - **Word (.docx)**: Para editar o modificar el certificado
   - **PDF (.pdf)**: Para imprimir o enviar directamente
4. Haga clic en "Generar Certificado PAA"
5. El sistema procesará el documento y descargará automáticamente el certificado en el formato seleccionado

## Tecnologías

- **Django**: Framework web
- **Gemini 2.5 Flash**: Modelo de IA para extracción de información
- **python-docx**: Manipulación de documentos Word
- **docx2pdf**: Conversión de Word a PDF (requiere Microsoft Word en Windows)
- **jQuery + AJAX**: Interfaz de usuario interactiva
- **SweetAlert2**: Notificaciones elegantes

## Estructura de Archivos

```
paa/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── urls.py
├── views.py
├── README.md
└── templates/
    └── paa/
        ├── index.html
        ├── plantilla_paa.docx  (debe crearse)
        └── README_PLANTILLA.md
```

## Notas Importantes

- El sistema usa Gemini 2.5 Flash (`gemini-2.0-flash-exp`) para máxima precisión
- La plantilla PAA NO debe ser modificada, solo los placeholders
- Todos los campos extraídos se convierten a MAYÚSCULAS
- La fecha se genera automáticamente en español
- El sistema valida que el archivo sea .docx

## Solución de Problemas

### Error: "No se ha configurado la variable de entorno GEMINI_API_KEY"
- Asegúrese de haber configurado la variable de entorno `GEMINI_API_KEY`
- Reinicie el servidor Django después de configurar la variable

### Error: "No se encontró la plantilla"
- Verifique que existe el archivo `plantilla_paa.docx` en la ruta correcta
- La ruta debe ser: `app/paa/templates/paa/plantilla_paa.docx`

### El certificado no se descarga
- Verifique que el navegador permita descargas automáticas
- Revise la consola del navegador para errores JavaScript

### Error: "La conversión a PDF no está disponible"
- Asegúrese de haber instalado `docx2pdf`: `pip install docx2pdf`
- En Windows, debe tener Microsoft Word instalado
- En Linux/Mac, considere usar alternativas como `libreoffice` con `subprocess`

### Error al convertir a PDF
- Verifique que Microsoft Word esté instalado y funcionando correctamente
- Cierre cualquier instancia de Word que esté abierta
- Intente reiniciar el servidor Django

## Mantenimiento

Para actualizar el modelo de Gemini, modifique la línea en `views.py`:

```python
model = genai.GenerativeModel('gemini-2.0-flash-exp')
```

Para cambiar el formato de fecha, modifique la función `generar_fecha_en_letras()` en `views.py`.
