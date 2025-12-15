# 🚀 Pasos Siguientes - Sistema de Gestión de Usuarios

## ✅ Lo que se ha implementado

Se ha creado un **sistema completo de gestión de usuarios** con las siguientes características:

### Funcionalidades Principales
- ✅ **Gestión completa de usuarios** (crear, editar, ver, activar/desactivar)
- ✅ **Control de permisos por módulos** (cada usuario solo ve los módulos asignados)
- ✅ **Contraseñas temporales** con cambio obligatorio en primer login
- ✅ **Usuario basado en número de ID** (cédula)
- ✅ **Recuperación de contraseña por email**
- ✅ **Roles**: Superusuario, Administrador de Usuarios, Usuario Regular
- ✅ **Auditoría completa** (quién creó, cuándo, última modificación)

### Tu Usuario (Superusuario)
- ✅ Tendrás **acceso total** a todos los módulos
- ✅ Podrás **crear y gestionar usuarios**
- ✅ Podrás **asignar permisos** por módulo a cada usuario

### Ejemplo de Uso
**Usuario "Andrés"** → Solo acceso al módulo **PAA**
- Verá únicamente el menú de PAA
- No podrá acceder a Contratación, Proveedores, etc.
- Intentar acceder a otros módulos mostrará error de permisos

---

## 📋 PASOS OBLIGATORIOS PARA ACTIVAR EL SISTEMA

### 1️⃣ Crear las Migraciones de Base de Datos

```bash
cd c:\Users\danie\OneDrive - SENA\Documentos\Dev\cividata_edenorte\app
python manage.py makemigrations login
python manage.py migrate
```

**Esto creará las tablas:**
- `login_modulo` (módulos del sistema)
- `login_perfilusuario` (perfiles extendidos de usuarios)
- Tablas relacionales para permisos

### 2️⃣ Inicializar los Módulos del Sistema

```bash
python manage.py inicializar_modulos
```

**Este comando:**
- Crea los 7 módulos del sistema (Contratación, PAA, Proveedores, etc.)
- Configura automáticamente tu usuario actual como superusuario
- Te da permisos para gestionar usuarios

### 3️⃣ Configurar Email (OPCIONAL pero recomendado)

Si quieres que se envíen contraseñas temporales por email, configura estas variables de entorno:

**Opción A: Archivo `.env`** (crear en la raíz del proyecto)
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion
DEFAULT_FROM_EMAIL=tu_correo@gmail.com
```

**Opción B: Variables de entorno del sistema**

**IMPORTANTE para Gmail:**
- No uses tu contraseña normal
- Crea una "Contraseña de aplicación" en tu cuenta de Google
- Ve a: Cuenta de Google → Seguridad → Verificación en 2 pasos → Contraseñas de aplicaciones

**Si NO configuras email:**
- El sistema funcionará igual
- La contraseña temporal se mostrará en pantalla al crear usuarios
- Deberás copiarla y enviarla manualmente al usuario

### 4️⃣ Verificar tu Usuario como Superusuario

Después de ejecutar `inicializar_modulos`, verifica que tu usuario esté configurado:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

# Ver tu usuario
user = User.objects.get(username='tu_usuario_actual')
print(f"Superusuario del sistema: {user.perfil.es_superusuario_sistema}")
print(f"Puede gestionar usuarios: {user.perfil.puede_gestionar_usuarios}")
print(f"Número ID: {user.perfil.numero_id}")

# Si necesitas actualizar algo:
perfil = user.perfil
perfil.numero_id = 'TU_CEDULA'  # Tu número de cédula
perfil.es_superusuario_sistema = True
perfil.puede_gestionar_usuarios = True
perfil.password_temporal = False
perfil.save()
```

---

## 🎯 Cómo Usar el Sistema

### Como Superusuario (TÚ)

#### 1. Acceder a Gestión de Usuarios
- Inicia sesión normalmente
- Clic en tu nombre (esquina superior derecha)
- Selecciona **"Gestionar Usuarios"**

#### 2. Crear un Nuevo Usuario (Ejemplo: Andrés)

**Paso a paso:**
1. Clic en **"Crear Nuevo Usuario"**
2. Llenar el formulario:
   - **Nombres**: Andrés
   - **Apellidos**: Ocampo Castaño
   - **Número de Identificación**: 12345678 (este será su usuario)
   - **Email**: andres@ejemplo.com
   - **Cargo**: Profesional Universitario
   - **Departamento**: Sistemas
   - **Módulos Permitidos**: ☑️ Solo marcar **PAA**
   - **Puede Gestionar Usuarios**: ☐ Dejar desmarcado

3. Clic en **"Crear Usuario"**

**¿Qué sucede?**
- Se genera una contraseña temporal aleatoria (ej: `aB3$xY9zK2mP`)
- Se envía por email a andres@ejemplo.com (si configuraste email)
- O se muestra en pantalla para que la copies

#### 3. El Usuario Andrés Inicia Sesión por Primera Vez

1. Va a la página de login
2. Ingresa:
   - **Usuario**: `12345678` (su número de ID)
   - **Contraseña**: `aB3$xY9zK2mP` (la temporal)
3. El sistema lo redirige **automáticamente** a cambiar contraseña
4. Debe ingresar:
   - Contraseña temporal
   - Nueva contraseña (2 veces)
5. Después de cambiarla, ya puede usar el sistema

#### 4. Andrés Solo Ve el Módulo PAA

- En el menú lateral solo verá: **"Asistente Contratación → PAA"**
- NO verá: Contratación, Proveedores, Reportes, etc.
- Si intenta acceder a una URL de otro módulo, verá error de permisos

---

## 🔐 Niveles de Permisos

### 1. Superusuario del Sistema (TÚ)
- ✅ Acceso a **TODOS** los módulos
- ✅ Puede crear y gestionar usuarios
- ✅ Puede asignar permisos
- ✅ No puede ser desactivado
- ✅ No necesita módulos asignados (acceso automático)

### 2. Administrador de Usuarios
- ✅ Puede crear y gestionar usuarios
- ⚠️ Solo ve los módulos que le asignes
- ✅ Puede resetear contraseñas de otros usuarios

### 3. Usuario Regular (Ejemplo: Andrés)
- ⚠️ Solo ve los módulos asignados
- ❌ No puede gestionar usuarios
- ✅ Puede cambiar su propia contraseña

---

## 📱 Funciones Disponibles

### Para Superusuarios/Administradores

#### Crear Usuario
`/login/usuarios/crear/`

#### Ver Lista de Usuarios
`/login/usuarios/`

#### Ver Detalle de Usuario
`/login/usuarios/<id>/`

#### Editar Usuario
`/login/usuarios/<id>/editar/`

#### Resetear Contraseña
`/login/usuarios/<id>/resetear-password/`

#### Activar/Desactivar Usuario
`/login/usuarios/<id>/toggle-activo/` (AJAX)

### Para Todos los Usuarios

#### Cambiar Mi Contraseña
`/login/cambiar-password/`

#### Primer Cambio de Contraseña (Automático)
`/login/primer-cambio-password/`

---

## 🛠️ Comandos Útiles

```bash
# Ver todos los usuarios
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()

# Ver módulos creados
>>> from login.models import Modulo
>>> Modulo.objects.all()

# Ver perfil de un usuario
>>> user = User.objects.get(username='12345678')
>>> user.perfil.modulos_permitidos.all()

# Asignar módulo a usuario
>>> from login.models import Modulo
>>> modulo_paa = Modulo.objects.get(codigo='paa')
>>> user.perfil.modulos_permitidos.add(modulo_paa)

# Dar permisos de gestión de usuarios
>>> user.perfil.puede_gestionar_usuarios = True
>>> user.perfil.save()
```

---

## ⚠️ Solución de Problemas Comunes

### Error: "No se encontró la tabla login_modulo"
**Solución:** Ejecuta las migraciones
```bash
python manage.py makemigrations login
python manage.py migrate
```

### Error: "No tienes permisos para gestionar usuarios"
**Solución:** Ejecuta el comando de inicialización
```bash
python manage.py inicializar_modulos
```

### No se envían los emails
**Solución:** 
- Verifica configuración de EMAIL en settings.py
- Si usas Gmail, crea contraseña de aplicación
- El sistema mostrará la contraseña en pantalla como respaldo

### Usuario no ve ningún módulo
**Solución:**
- Asigna al menos un módulo al usuario
- O márcalo como superusuario del sistema

---

## 📚 Archivos de Documentación

- **`GESTION_USUARIOS_README.md`**: Documentación técnica completa
- **`PASOS_SIGUIENTES.md`**: Este archivo (guía rápida)

---

## ✨ Próximos Pasos Recomendados

1. ✅ Ejecutar migraciones
2. ✅ Ejecutar `inicializar_modulos`
3. ✅ Configurar email (opcional)
4. ✅ Crear tu primer usuario de prueba
5. ✅ Probar el flujo completo de login con contraseña temporal
6. ✅ Asignar módulos específicos y verificar que funcione el control de acceso

---

## 🎉 ¡Listo!

El sistema está completamente implementado y listo para usar. Solo necesitas ejecutar los 2 comandos obligatorios y ya podrás gestionar usuarios con control de permisos por módulos.

**¿Dudas?** Revisa `GESTION_USUARIOS_README.md` para documentación técnica detallada.
