# 🔑 Manual: Gestión Administrativa y Registro de Modelos Multi-Tenant (Django Admin)

Este documento detalla los procedimientos técnicos para la creación de credenciales de acceso maestro y la configuración de la interfaz administrativa de Django. Se implementa un esquema de enrutamiento explícito para gestionar simultáneamente la base de datos de administración (`default`) y la base de datos de inquilinos (`tenant`) desde un único panel de control.

Estas acciones permiten gestionar la base de datos de forma intuitiva sin necesidad de ejecutar comandos SQL manuales.

---

## 1. Creación de Superusuario (Acceso Maestro)

El Superusuario constituye la cuenta de máxima jerarquía. En la arquitectura Multi-Tenant, este usuario reside estrictamente en la base de datos `default` (Puerta 1), vinculado al modelo `AdminUser`.


### Requisitos Previos
* El entorno virtual (`venv`) debe estar activo.
* Se debe haber ejecutado la persistencia inicial (`python manage.py migrate`) para que las tablas residan físicamente en el motor de base de datos.

### Procedimiento en Terminal
Ejecute el siguiente comando en la raíz del proyecto:

```bash
python manage.py createsuperuser
```

### Secuencia de Captura de Datos
El sistema solicitará los parámetros definidos en el modelo `AdminUser`:
1. **Username:** Identificador de acceso.
2. **Correo Electrónico:** Dirección de correo (campo obligatorio y único).
3. **Password:** Clave de seguridad (mínimo 8 caracteres).
4. **Password (again):** Confirmación de la clave de seguridad.

> **Nota de Seguridad:** Durante la digitación de la contraseña, la interfaz de línea de comandos no renderizará caracteres visibles. Se debe ingresar el valor y oprimir la tecla de retorno.

---

## 2. Configuración del Panel Administrativo (admin.py)

Para exponer los modelos personalizados en la interfaz web de Django y garantizar que las transacciones afecten a las bases de datos correctas, es imperativo configurar los archivos `admin.py` de cada dominio.

### A. Registro de la Puerta 1 (Dominio Administración)
El modelo `AdminUser` hereda de `AbstractUser`. Su registro requiere extender la clase `UserAdmin` nativa de Django para inyectar los campos personalizados.

**Archivo:** `apps/admin/admin_users/admin.py`

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AdminUser

class CustomAdminUserAdmin(UserAdmin):
    # Columnas expuestas en la vista de lista
    list_display = ('username', 'email', 'cargo_interno', 'is_staff')
    
    # Inyección de campos personalizados en la vista de detalle
    fieldsets = UserAdmin.fieldsets + (
        ('Información Interna ERP', {
            'fields': ('cargo_interno', 'telefono_contacto')
        }),
    )

# Registro del modelo en el ecosistema Admin
admin.site.register(AdminUser, CustomAdminUserAdmin)
```

### B. Registro de la Puerta 2 (Dominio Inquilinos)
Dado que el panel administrativo de Django ejecuta sus sentencias por defecto sobre la base de datos `default`, es obligatorio implementar una clase controladora (`TenantModelAdmin`) que fuerce el enrutamiento de las consultas (QuerySets) y transacciones (Save/Delete) hacia la base de datos `tenant`.

**Archivo:** `apps/tenant/tenant_users/admin.py`

```python
from django.contrib import admin
from .models import TenantUser, TenantRol, TenantPermission

class TenantModelAdmin(admin.ModelAdmin):
    """
    Controlador maestro para forzar el enrutamiento de operaciones
    del panel administrativo hacia la base de datos 'tenant'.
    """
    using = 'tenant'

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


class TenantUserAdmin(TenantModelAdmin):
    # Configuración de visualización para el modelo AbstractBaseUser
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'date_joined')
    ordering = ('-date_joined',)

# Registro de entidades bajo la regla de enrutamiento estricto
admin.site.register(TenantUser, TenantUserAdmin)
admin.site.register(TenantRol, TenantModelAdmin)
admin.site.register(TenantPermission, TenantModelAdmin)
```

---

## 3. Protocolo de Validación y Puesta en Marcha

Para auditar el correcto funcionamiento de las políticas de enrutamiento y la renderización de la interfaz:

1. **Reinicio de Instancia:** Confirmar la persistencia de los archivos modificados y asegurar que el servidor de desarrollo se encuentre en ejecución (`python manage.py runserver`).
2. **Autenticación Web:** Acceder al recurso `http://127.0.0.1:8000/portal-maestro-volt/` mediante el navegador web e ingresar con las credenciales de Superusuario previamente generadas.
3. **Auditoría Estructural:**
   * Localizar el grupo **Admin_Users**. Ingresar al perfil creado y constatar la existencia del bloque **"Información Interna ERP"** conteniendo los atributos `cargo_interno` y `telefono_contacto`.
   * Localizar el grupo **Tenant_Users**. Verificar la operatividad de los listados de **Usuarios Inquilinos**, **Roles de Inquilinos** y **Permisos de Inquilinos**.
4. **Prueba de Escritura Aislada:** Crear un registro de prueba en `TenantUser` y verificar mediante herramientas de inspección (ej. pgAdmin) que el registro se ha almacenado físicamente en la base de datos `erp_tenant_db` y no en `erp_admin_db`.

---
© 2026 - Proyecto ERP Colombiano - Arquitectura Multi-Tenant.