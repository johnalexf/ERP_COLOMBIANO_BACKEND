# 🔑 Manual: Gestión Administrativa y Registro de Modelos (Django Admin)

Este documento detalla los pasos para crear la cuenta de control total y configurar el panel visual de administración. Estas acciones permiten gestionar la base de datos de forma intuitiva sin necesidad de ejecutar comandos SQL manuales.

---

## 1. Creación de Superusuario (Acceso Maestro)
El Superusuario es la cuenta con privilegios totales. Es el primer paso tras realizar las migraciones, ya que habilita la entrada a la "Torre de Control" del sistema.

### Requisitos Previos
* El entorno virtual (`venv`) debe estar activo.
* Se debe haber ejecutado la persistencia inicial (`python manage.py migrate`) para que las tablas residan físicamente en el motor de base de datos.

### Procedimiento en Terminal
Ejecute el siguiente comando en la raíz del proyecto:

```bash
python manage.py createsuperuser
```

### Flujo de Datos solicitado:
El sistema solicitará los siguientes campos de forma secuencial:
1. **Username:** Identificador de acceso (ej: `admin`).
2. **Email address:** Correo electrónico de contacto (puede dejarse vacío presionando Enter).
3. **Password:** Contraseña de acceso (mínimo 8 caracteres).
4. **Password (again):** Confirmación de la contraseña.

> [!IMPORTANT]
> **Privacidad de Entrada:** Por seguridad, al escribir la contraseña la terminal no mostrará caracteres ni asteriscos. Se debe digitar la clave con normalidad y presionar Enter.

---

## 2. Configuración del Panel Administrativo (admin.py)
Por defecto, Django no muestra los modelos personalizados en la interfaz web. Para visualizarlos, es necesario realizar un "registro de vitrina" en los archivos correspondientes.

### A. Personalización del Modelo de Usuario
Para visualizar los campos adicionales (Cédula, Empresa, Cargo) en el panel, se debe extender la configuración estándar.

**Archivo:** `apps/users/admin.py`

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Extensión de la interfaz para el Usuario Personalizado
class CustomUserAdmin(UserAdmin):
    # Columnas visibles en el listado general
    list_display = ('username', 'email', 'cedula', 'empresa', 'is_staff')
    
    # Organización de los campos en el formulario de edición (Detalle)
    # Se mantienen los campos estándar y se anexa la "Información de Negocio"
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Negocio', {
            'fields': ('cedula', 'telefono', 'cargo', 'empresa')
        }),
    )

# Registro del modelo bajo la nueva configuración
admin.site.register(User, CustomUserAdmin)
```

### B. Registro de Modelos de Negocio (Inventario)
Para tablas estándar que no requieren visualizaciones complejas, se realiza un registro directo.

**Archivo: de ejemplo** `apps/inventario/admin.py`

```python
from django.contrib import admin
from .models import Producto, Empresa, Bodega

# Registro de entidades para gestión visual
admin.site.register(Producto)
admin.site.register(Empresa)
admin.site.register(Bodega)
```

---

## 3. Protocolo de Validación y Puesta en Marcha
Para asegurar que el "Tablero de Control" refleja los cambios, siga estos pasos:

1. **Reinicio del Servicio:** Guardar todos los archivos y verificar que el servidor de desarrollo se refresque correctamente.
2. **Acceso Web:** Ingresar en el navegador a: `http://127.0.0.1:8000/admin`
3. **Autenticación:** Utilizar las credenciales creadas en el paso de **Superusuario**.
4. **Inspección Visual:** * Localizar la sección **Users**.
   * Ingresar a un perfil y validar que aparezca el bloque **"Información de Negocio"** con los campos de Cédula, Teléfono y Cargo.
   * Verificar que los módulos de **Productos, Empresas y Bodegas** aparezcan listados y permitan crear nuevos registros.

> [!TIP]
> **Resolución de Conflictos:** Si el servidor arroja un error al iniciar, verifique que los nombres de los modelos importados en `admin.py` coincidan letra por letra con los definidos en `models.py`.

---
© 2026 - Proyecto ERP Colombiano - Desarrollo Profesional.