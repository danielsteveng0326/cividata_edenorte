# Sistema de Gestión de Usuarios - CiviData Edenorte

## Descripción General

Sistema completo de gestión de usuarios con control de permisos por módulos, contraseñas temporales, y recuperación por email.

## Características Implementadas

### 1. **Gestión de Usuarios**
- ✅ Crear nuevos usuarios con contraseña temporal
- ✅ Editar información de usuarios existentes
- ✅ Ver detalles completos de usuarios
- ✅ Activar/Desactivar usuarios
- ✅ Resetear contraseñas
- ✅ Usuario basado en número de identificación (ID)

### 2. **Sistema de Permisos por Módulos**
- ✅ Control granular de acceso a módulos
- ✅ Superusuarios con acceso total
- ✅ Usuarios administradores que pueden gestionar otros usuarios
- ✅ Usuarios regulares con módulos específicos asignados

### 3. **Contraseñas Temporales**
- ✅ Generación automática de contraseñas seguras
- ✅ Cambio obligatorio en primer inicio de sesión
- ✅ Middleware que fuerza el cambio de contraseña
- ✅ Envío por email de contraseñas temporales

### 4. **Recuperación de Contraseña**
- ✅ Reseteo de contraseña por administradores
- ✅ Envío automático por email
- ✅ Nueva contraseña temporal generada

### 5. **Módulos del Sistema**
Los siguientes módulos están disponibles para asignar:
- **Contratación**: Gestión de contratos y contratación
- **Asistente Contratación**: Herramientas asistidas
- **PAA**: Plan Anual de Adquisiciones
- **Documentos Contractuales**: Generación automática
- **Proveedores**: Gestión de proveedores
- **Reportes**: Reportes y estadísticas
- **Chatbot Emil-IA**: Asistente virtual

## Instalación y Configuración

### Paso 1: Crear Migraciones

```bash
python manage.py makemigrations login
python manage.py migrate
```

### Paso 2: Inicializar Módulos del Sistema

```bash
python manage.py inicializar_modulos
```

Este comando:
- Crea todos los módulos del sistema
- Configura automáticamente los superusuarios existentes
- Asigna permisos de gestión de usuarios

### Paso 3: Configurar Email (Opcional pero Recomendado)

Agrega las siguientes variables de entorno en tu archivo `.env` o configuración:

```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion
DEFAULT_FROM_EMAIL=tu_correo@gmail.com
```

**Nota para Gmail**: Necesitas crear una "Contraseña de aplicación" en tu cuenta de Google.

### Paso 4: Configurar tu Usuario como Superusuario

Si ya tienes un usuario creado, actualiza su perfil:

```python
from django.contrib.auth.models import User
from login.models import PerfilUsuario

# Obtener tu usuario
user = User.objects.get(username='tu_usuario')

# Configurar perfil
perfil = user.perfil
perfil.numero_id = 'TU_NUMERO_ID'  # Tu número de cédula
perfil.es_superusuario_sistema = True
perfil.puede_gestionar_usuarios = True
perfil.password_temporal = False
perfil.save()
```

## Uso del Sistema

### Como Superusuario

1. **Acceder a Gestión de Usuarios**
   - Clic en tu nombre (esquina superior derecha)
   - Seleccionar "Gestionar Usuarios"

2. **Crear Nuevo Usuario**
   - Ir a "Gestión de Usuarios"
   - Clic en "Crear Nuevo Usuario"
   - Llenar formulario con:
     - Nombres y apellidos
     - Número de identificación (será el usuario)
     - Email (para recibir contraseña temporal)
     - Cargo y departamento (opcional)
     - Seleccionar módulos permitidos
     - Marcar si puede gestionar usuarios

3. **Editar Usuario**
   - En la lista de usuarios, clic en el botón "Editar" (lápiz)
   - Modificar información necesaria
   - Guardar cambios

4. **Resetear Contraseña**
   - En detalle de usuario, clic en "Resetear Contraseña"
   - Se genera nueva contraseña temporal
   - Se envía por email al usuario

### Como Usuario Regular

1. **Primer Inicio de Sesión**
   - Usar número de ID como usuario
   - Ingresar contraseña temporal recibida por email
   - Sistema redirige automáticamente a cambio de contraseña
   - Establecer nueva contraseña segura

2. **Cambiar Contraseña**
   - Clic en tu nombre (esquina superior derecha)
   - Seleccionar "Cambiar Contraseña"
   - Ingresar contraseña actual
   - Ingresar nueva contraseña dos veces

3. **Acceso a Módulos**
   - Solo verás en el menú los módulos asignados
   - Intentar acceder a módulos no permitidos mostrará error

## Estructura de Permisos

### Niveles de Usuario

1. **Superusuario del Sistema**
   - Acceso total a todos los módulos
   - Puede gestionar usuarios
   - No puede ser desactivado
   - Configurado en `perfil.es_superusuario_sistema = True`

2. **Administrador de Usuarios**
   - Puede crear y gestionar usuarios
   - Acceso solo a módulos asignados
   - Configurado en `perfil.puede_gestionar_usuarios = True`

3. **Usuario Regular**
   - Acceso solo a módulos asignados
   - No puede gestionar usuarios
   - Puede cambiar su propia contraseña

## Archivos Creados/Modificados

### Nuevos Archivos
```
login/
├── models.py (actualizado con Modulo y PerfilUsuario)
├── forms.py (formularios de gestión)
├── decorators.py (control de acceso)
├── context_processors.py (permisos en templates)
├── middleware_password.py (forzar cambio de contraseña)
├── admin.py (actualizado)
├── management/
│   └── commands/
│       └── inicializar_modulos.py

templates/login/
├── lista_usuarios.html
├── crear_usuario.html
├── editar_usuario.html
├── detalle_usuario.html
├── resetear_password.html
├── cambiar_password.html
└── primer_cambio_password.html
```

### Archivos Modificados
```
- app/settings.py (middleware, email, context processor)
- login/views.py (nuevas vistas)
- login/urls.py (nuevas rutas)
- templates/navbar.html (menú de usuarios)
```

## Seguridad

### Contraseñas Temporales
- Generadas con 12 caracteres aleatorios
- Incluyen letras, números y símbolos especiales
- Cambio obligatorio en primer inicio de sesión

### Control de Acceso
- Decoradores `@puede_gestionar_usuarios_required`
- Decoradores `@modulo_required('codigo_modulo')`
- Middleware que verifica contraseña temporal
- Context processor para permisos en templates

### Auditoría
- Registro de quién creó cada usuario
- Fechas de creación y modificación
- Historial de cambios de contraseña

## Solución de Problemas

### Error: "No se pudo enviar el correo"
- Verificar configuración de EMAIL en settings.py
- Verificar credenciales de email
- Si usas Gmail, crear contraseña de aplicación
- El sistema mostrará la contraseña temporal en pantalla como respaldo

### Error: "No tienes permisos para gestionar usuarios"
- Verificar que `perfil.puede_gestionar_usuarios = True`
- O que `perfil.es_superusuario_sistema = True`
- Ejecutar comando `inicializar_modulos` si es superusuario Django

### Usuario no puede acceder a módulo
- Verificar que el módulo esté activo en base de datos
- Verificar que el módulo esté asignado al usuario
- Si es superusuario, debe tener acceso automático

### Middleware de contraseña no funciona
- Verificar que esté en MIDDLEWARE en settings.py
- Debe estar después de AuthenticationMiddleware
- Verificar que `perfil.password_temporal = True`

## Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations login

# Aplicar migraciones
python manage.py migrate

# Inicializar módulos
python manage.py inicializar_modulos

# Crear superusuario (Django admin)
python manage.py createsuperuser

# Acceder a shell de Django
python manage.py shell
```

## Ejemplo de Uso en Shell

```python
from django.contrib.auth.models import User
from login.models import PerfilUsuario, Modulo

# Crear usuario programáticamente
user = User.objects.create_user(
    username='12345678',
    email='usuario@ejemplo.com',
    first_name='Juan',
    last_name='Pérez'
)
user.set_password('temporal123')
user.save()

# Configurar perfil
perfil = user.perfil
perfil.numero_id = '12345678'
perfil.cargo = 'Analista'
perfil.password_temporal = True
perfil.save()

# Asignar módulos
modulo_paa = Modulo.objects.get(codigo='paa')
perfil.modulos_permitidos.add(modulo_paa)
```

## Próximas Mejoras Sugeridas

- [ ] Historial de cambios de permisos
- [ ] Notificaciones por email de cambios importantes
- [ ] Exportación de lista de usuarios a Excel
- [ ] Filtros avanzados en lista de usuarios
- [ ] Gráficas de usuarios por módulo
- [ ] Logs de acceso por usuario
- [ ] Sesiones concurrentes por usuario
- [ ] Autenticación de dos factores (2FA)

## Soporte

Para problemas o preguntas, contactar al administrador del sistema.
