# 📖 Documentación Automática de la API (Swagger & OpenAPI)

Este documento describe la implementación de un sistema de documentación dinámica. Su objetivo es generar un portal interactivo donde el equipo de Frontend (React) pueda consultar, probar y validar cada punto de acceso (Endpoint) de la API sin necesidad de revisar el código fuente.

---

## 1. Instalación del Generador de Esquemas
Se utiliza `drf-spectacular`, una herramienta que escanea la arquitectura del proyecto y extrae automáticamente las rutas, parámetros y tipos de respuesta.

```bash
# Ejecutar con el entorno virtual (venv) activo:

# 1. Instalar la librería
pip install drf-spectacular

# 2. Actualizar la bitácora de dependencias (¡Paso Vital!)
pip freeze > requirements.txt
```

---

## 2. Registro en el Núcleo (Settings)
Se debe informar al sistema sobre la presencia de esta nueva herramienta en `core/settings.py`.

* **Agregar en INSTALLED_APPS:**
```python
INSTALLED_APPS = [
    # ... otras aplicaciones ...
    'drf_spectacular',
]
```

* **Vincular con Django REST Framework:**
Dentro del bloque `REST_FRAMEWORK`, se debe definir a esta librería como la encargada de generar el esquema técnico.

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema', # <--- AGREGAR ESTA LÍNEA
}
```

---

## 3. Configuración del "Catálogo" (Metadatos)
Para que el portal sea profesional, se deben definir los títulos y descripciones que verá el equipo de desarrollo. Agregar este bloque al final de `core/settings.py`.

```python
# --- CONFIGURACIÓN DE DOCUMENTACIÓN SWAGGER ---
SPECTACULAR_SETTINGS = {
    'TITLE': 'ERP Colombiano API',
    'DESCRIPTION': 'Documentación interactiva de los servicios del ERP. Incluye gestión de usuarios y autenticación JWT.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # Permite que la documentación use el botón de "Authorize" con Tokens JWT
    'COMPONENT_SPLIT_PATCH': True,
    'COMPONENT_SPLIT_REQUEST': True,
}
```

---

## 4. Activación de Puntos de Acceso Visuales
Se deben crear las direcciones físicas donde se podrá consultar el portal. Se recomienda configurar tres rutas: el archivo técnico (esquema), el portal visual (Swagger) y una alternativa (Redoc).

**Archivo:** `core/urls.py`

```python
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)

urlpatterns = [
    # ... rutas anteriores (admin, api/users) ...

    # Rutas de Documentación Automática
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'), # El archivo técnico base
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), # El portal interactivo
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), # Vista alternativa
]
```

---

## 5. 🧪 Verificación y Uso Interactivo
Una vez realizados los cambios y con el servidor en ejecución (`python manage.py runserver`), se debe ingresar a la siguiente dirección en el navegador:

👉 **[http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)**

### Justificación Técnica: Ventajas del Portal
* **Pruebas en tiempo real:** Cada sección cuenta con un botón **"Try it out"**, permitiendo enviar datos a la base de datos de PostgreSQL directamente desde el navegador.
* **Filtros de Seguridad:** En la parte superior derecha, el botón **"Authorize"** permite pegar el Token JWT para probar rutas protegidas sin usar Postman.
* **Contrato de Interfaz:** El equipo de React podrá ver exactamente qué campos son obligatorios y qué tipo de dato (número, texto o fecha) requiere cada "cajón" de la base de datos.

---

---

## 6. 📄 Generación de Documentos Técnicos (Exportación)

Una vez que la documentación interactiva está operativa, se pueden generar archivos físicos para entregas oficiales o para que el equipo de Frontend los importe en sus herramientas de trabajo.

### A. Exportar el "Contrato de Interfaz" (YAML)
Este archivo es el estándar industrial que describe cada punto de acceso (Endpoint) de la API. Es ideal para compartirlo con otros desarrolladores.

```bash
# Ejecutar en la terminal con el entorno virtual activo:
python manage.py spectacular --file coleccion_postman_api.yml
```
> **Utilidad:** Este archivo `.yml` puede ser importado directamente en **Postman** o **Insomnia** para generar automáticamente todas las colecciones de prueba sin escribir una sola URL manualmente.

#### Procedimiento de Importación en Postman
Una vez generado el archivo `coleccion_postman_api.yml`, siga estos pasos para automatizar la creación de las pruebas:

1. **Abrir Postman:** En la esquina superior izquierda de la aplicación, haga clic en el botón **"Import"** (o presione `Ctrl + O`).
2. **Seleccionar el Archivo:** Arrastre el archivo `.yml` generado o selecciónelo desde su carpeta de archivos.
3. **Configuración de Importación:** * Postman detectará automáticamente el formato como **OpenAPI 3.0**.
   * Asegúrese de marcar la opción **"Generate a Collection"** (Generar una colección).
   * Haga clic en el botón **"Import"**.
4. **Resultado:** En el panel izquierdo, en la sección de **Collections**, aparecerá una nueva carpeta llamada `ERP Colombiano API` con todas las rutas (`GET`, `POST`, `PATCH`, `DELETE`) ya creadas y listas para ser probadas.



> [!TIP]
> **Sincronización de Cambios:** > Si en el futuro agrega nuevos módulos al ERP (como Inventarios o Ventas), simplemente genere un nuevo archivo YAML y repita este proceso. Postman actualizará la colección con los nuevos puntos de acceso, garantizando que el equipo de desarrollo siempre trabaje con la versión más reciente del sistema.
---


### B. Vista de Lectura Profesional (Redoc)
Si el equipo prefiere una documentación tipo "libro técnico" o manual de referencia (más organizada y menos interactiva que Swagger), se debe acceder a:

👉 **[http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)**



### C. Generación de Manual en PDF
Para obtener un documento estático que se pueda enviar por correo o adjuntar a un informe de avance:

1. Ingrese a la ruta de **Swagger** (`/api/docs/`) o **Redoc** (`/api/redoc/`).
2. Presione `Ctrl + P` (Imprimir).
3. Seleccione la opción **"Guardar como PDF"**. 
4. El sistema ajustará automáticamente el diseño para que el manual sea legible y profesional.

---

## 7. 🧠 Resumen de Beneficios para el Proyecto
* **Sincronización Total:** Si se agrega un nuevo campo al modelo (ej. `fecha_nacimiento`), la documentación se actualiza sola al guardar los cambios.
* **Reducción de Errores:** El Frontend sabe exactamente qué "llave" (Key) esperar en el JSON, evitando fallos por nombres mal escritos.
* **Pruebas Rápidas:** Permite validar la lógica de negocio sin haber escrito una sola línea de código en React.

---
© 2026 - Proyecto ERP Colombiano - Desarrollo Profesional.
