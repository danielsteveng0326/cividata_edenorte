# app/proveedor/__init__.py
"""
Módulo de Gestión de Proveedores

Este módulo permite:
- Consultar proveedores por NIT a través de API de SECOP (datos.gov.co)
- Registrar proveedores manualmente siguiendo el patrón de dashboard
- Gestionar información de proveedores y representantes legales
- Sincronización masiva desde RUP usando Socrata
- Validar y actualizar datos de proveedores existentes

Integración con:
- API de datos.gov.co usando Socrata (mismo patrón que dashboard/utils.py)
- Base de datos PostgreSQL siguiendo estructura de dashboard/models.py
- AdminLTE para interfaz siguiendo el estilo del proyecto
"""

default_app_config = 'proveedor.apps.ProveedorConfig'