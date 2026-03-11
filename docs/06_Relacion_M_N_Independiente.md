# 🏗️ Manual 06: Relación Muchos a Muchos (M:N) - Ciclo Completo Independiente

Este documento detalla la creación desde cero de dos módulos autónomos (**Productos** y **Bodegas**) y su posterior vinculación. Este esquema permite que un producto resida en múltiples sedes y que cada sede gestione un catálogo variado de productos.

---

## 1. ⚡ Preparación y Creación de Módulos (Apps)

Antes de escribir código, debemos asegurar que el entorno de trabajo esté listo y generar la estructura de carpetas para cada responsabilidad.

> [!IMPORTANT]
> **Estado Crítico:** Asegúrese de tener el indicador `(venv)` al inicio de su terminal. Si no aparece, ejecute: `.\venv\Scripts\activate`.

```bash
# 1. Ingresar a la carpeta de aplicaciones
cd apps

# 2. Crear la App de Productos (Catálogo maestro)
django-admin startapp productos

# 3. Crear la App de Bodegas (Sedes físicas)
django-admin startapp bodegas

# 4. Regresar a la raíz para futuros comandos
cd ..
```

---

## 2. 🧱 Definición de Estructuras (Modelos)

Diseñaremos los "cajones" donde se guardará la información. Aquí responderemos por qué usamos comillas en la relación.

### A. Modelo de Productos
**Archivo:** `apps/productos/models.py`
```python
from django.db import models

class Producto(models.Model):
    # Campos básicos del ítem
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    sku = models.CharField(max_length=50, unique=True, verbose_name="Código de Inventario")
    precio_base = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)

    def __str__(self):
        # Analogía: La etiqueta en la caja del producto para identificarlo rápido.
        return f"{self.nombre} ({self.sku})"
```

### B. Modelo de Bodegas (La Relación M:N)
**Archivo:** `apps/bodegas/models.py`
```python
from django.db import models

class Bodega(models.Model):
    nombre_sede = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255)

    # --- LA LLAVE MAESTRA (M:N) ---
    # Usamos 'productos.Producto' entre comillas por "Carga Perezosa" (Lazy Loading).
    # Esto evita tener que hacer un 'import' arriba, lo cual previene errores 
    # de importación circular si los archivos intentaran llamarse mutuamente.
    productos = models.ManyToManyField(
        'productos.Producto', 
        related_name='bodegas', 
        blank=True
    )

    def __str__(self):
        return self.nombre_sede
```

---

## 3. 🔄 Traductores de Datos (Serializers)

Configuramos cómo se convertirá la información de la base de datos a formato JSON para React.

**Archivo:** `apps/productos/serializers.py`
```python
from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__' # Expone: id, nombre, sku, precio_base
```

**Archivo:** `apps/bodegas/serializers.py`
```python
from rest_framework import serializers
from .models import Bodega
from apps.productos.serializers import ProductoSerializer # Importamos el traductor de productos

class BodegaSerializer(serializers.ModelSerializer):
    # many=True: Indica que 'productos' es una lista de objetos, no uno solo.
    # read_only=True: Para que al crear la bodega no nos obligue a meter productos de inmediato.
    productos_detalle = ProductoSerializer(source='productos', many=True, read_only=True)

    class Meta:
        model = Bodega
        fields = ['id', 'nombre_sede', 'ubicacion', 'productos', 'productos_detalle']
```

---

## 4. 🧠 Lógica y Puntos de Acceso (Views & URLs)

Habilitamos las "ventanillas de atención" de nuestra API para que Postman pueda interactuar con ellas.

### Vistas (Logic)
**Archivo:** `apps/productos/views.py` | **Archivo:** `apps/bodegas/views.py` (Misma estructura)
```python
from rest_framework import viewsets
from .models import TuModelo # Reemplazar por Producto o Bodega según corresponda
from .serializers import TuSerializer # Reemplazar por el serializador respectivo

class TuViewSet(viewsets.ModelViewSet):
    queryset = TuModelo.objects.all()
    serializer_class = TuSerializer
```

### Direcciones (URLs)
Se debe crear un archivo `urls.py` dentro de cada carpeta de app (`productos` y `bodegas`) con este esquema:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TuViewSet

router = DefaultRouter()
router.register(r'', TuViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

**REGISTRO EN EL NÚCLEO (`core/urls.py`):**
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/productos/', include('apps.productos.urls')),
    path('api/bodegas/', include('apps.bodegas.urls')),
]
```

---

## 5. 🛠️ Persistencia en PostgreSQL

Ejecutamos los comandos para que Django fabrique las tablas físicas, incluyendo la **tabla intermedia invisible** que unirá productos y bodegas.

```bash
# 1. Registrar cambios de ambos módulos
python manage.py makemigrations productos
python manage.py makemigrations bodegas

# 2. Aplicar a la base de datos
python manage.py migrate
```

---

## 🧪 Guía de Pruebas en Postman (Protocolo de Operación)

Siga este orden para validar que todo el "cableado" de la relación M:N funciona correctamente:

### Paso 1: Crear la Base de Datos
* **POST** `/api/productos/` -> `{"nombre": "Martillo", "sku": "M-01"}`
* **POST** `/api/bodegas/` -> `{"nombre_sede": "Sede Norte", "ubicacion": "Calle 10"}`

### Paso 2: Vincular Producto a Bodega (La Relación)
Para unir un producto con una bodega, realizamos una edición (`PATCH`) sobre la bodega enviando el ID del producto en una lista.

* **PATCH** `/api/bodegas/1/` (Asumiendo que es la Sede Norte con ID 1)
* **Body (JSON):** 
```json
{
    "productos": [1] 
}
```

### Paso 3: Verificación de Resultados
* **GET** `/api/bodegas/1/`
* **Respuesta Exitosa:**

```json
{
    "id": 1,
    "nombre_sede": "Sede Norte",
    "productos": [1],
    "productos_detalle": [
        {
            "id": 1,
            "nombre": "Martillo",
            "sku": "M-01"
        }
    ]
}
```

---
© 2026 - Proyecto ERP Colombiano - Desarrollo Profesional.