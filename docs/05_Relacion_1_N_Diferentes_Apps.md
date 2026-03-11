# 🏗️ Relación Uno a Muchos (1:N) - Entre Diferentes Apps

Este documento detalla el procedimiento para conectar dos módulos independientes del ERP. El caso de estudio es la relación entre **Empresa** y **Usuarios**, donde una empresa puede tener múltiples colaboradores vinculados, pero cada colaborador pertenece a una única razón social.

---

## 1. Creación de la Entidad Maestra (Empresa)
Primero debemos crear la aplicación independiente que gestionará los datos de las empresas.

```bash
# 1. Crear la nueva App
cd apps
django-admin startapp empresas
cd ..
```

**Archivo:** `apps/empresas/models.py`
```python
from django.db import models

class Empresa(models.Model):
    nit = models.CharField(max_length=20, unique=True)
    nombre_social = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre_social} - NIT: {self.nit}"
```

---

## 2. Configuración de la Llave Foránea (ForeignKey)
Ahora vinculamos el usuario con su empresa correspondiente. La "llave" de acceso se coloca en el modelo que depende del otro (el Usuario depende de la Empresa).

**Archivo:** `apps/users/models.py`

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # ... campos anteriores (cedula, cargo, etc.) ...

    # ForeignKey: Crea el vínculo 1:N.
    # on_delete=models.PROTECT: Impide borrar una empresa si aún tiene empleados activos.
    # related_name: Permite consultar desde empresa: mi_empresa.empleados.all()
    empresa_vinculada = models.ForeignKey(
        'empresas.Empresa', 
        on_delete=models.PROTECT, 
        related_name='empleados',
        null=True, 
        blank=True
    )
```
> **Nota de Seguridad:** Se utiliza `on_delete=models.PROTECT` para asegurar la integridad contable del ERP. Si una empresa tiene historial de usuarios, el sistema bloqueará cualquier intento de borrado accidental de la empresa.

---

## 3. Los Traductores (Serializers)

Necesitamos dos traductores: uno para gestionar las empresas y otro para los usuarios que las consumen.

**NUEVO Archivo:** `apps/empresas/serializers.py`
```python
from rest_framework import serializers
from .models import Empresa

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__' # Habilita todos los campos (id, nit, nombre, direccion)
```

**Archivo:** `apps/users/serializers.py` (Actualizado)
```python
class UserSerializer(serializers.ModelSerializer):
    # Campo de lectura para que React vea el nombre y no solo el ID
    nombre_empresa = serializers.CharField(source='empresa_vinculada.nombre_social', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'empresa_vinculada', 'nombre_empresa']
```

---

## 4. Lógica y Rutas (Views & URLs)

Para que el dueño del ERP pueda crear empresas, debemos habilitar los puntos de acceso.

**NUEVO Archivo:** `apps/empresas/views.py`
```python
from rest_framework import viewsets
from .models import Empresa
from .serializers import EmpresaSerializer

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
```

**NUEVO Archivo:** `apps/empresas/urls.py`
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpresaViewSet

router = DefaultRouter()
router.register(r'', EmpresaViewSet, basename='empresa')

urlpatterns = [
    path('', include(router.urls)),
]
```

**ACTUALIZACIÓN EN EL NÚCLEO:** `core/urls.py`
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/empresas/', include('apps.empresas.urls')), # <--- Registro Vital
]
```

---

## 5. Persistencia Cruzada (Migraciones)
Al modificar dos aplicaciones al mismo tiempo, el orden de las migraciones es vital.

```bash
# 1. Registrar los cambios de ambos módulos
python manage.py makemigrations empresas
python manage.py makemigrations users

# 2. Aplicar a la base de datos
python manage.py migrate
```

---

## 6. Protocolo de Pruebas en Postman (El Flujo Correcto)

Para que el sistema funcione, debe seguir este orden lógico:

| Paso | Acción | Método | Endpoint | Body JSON (Ejemplo) |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Crear Empresa** | `POST` | `/api/empresas/` | `{"nit": "900-1", "nombre_social": "Software SAS"}` |
| **2** | **Listar Empresas**| `GET` | `/api/empresas/` | (Verifica el `id` de la empresa creada) |
| **3** | **Asignar a User** | `PATCH` | `/api/users/1/` | `{"empresa_vinculada": 1}` |

> [!IMPORTANT]
> **Nota de Arquitectura:** Al habilitar el `EmpresaViewSet`, el Frontend de React ahora puede tener un formulario de "Crear Empresa" y un "Selector" (Dropdown) que consuma `/api/empresas/` para que el usuario elija su razón social fácilmente.

---
© 2026 - Proyecto ERP Colombiano - Desarrollo Profesional.

