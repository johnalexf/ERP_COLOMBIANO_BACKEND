# 🚀 ERP Colombiano - Backend Multi-Tenant (Django REST Framework)

Este proyecto es el núcleo de servicios (Backend) para el sistema de gestión ERP. Construido sobre Django REST Framework, implementa una arquitectura Multi-Tenant que garantiza la separación de datos y autenticación entre la administración global y los inquilinos (empresas).


## 🛠️ Guía de Inicialización

Siga estos pasos para replicar el entorno de desarrollo en su máquina local.

### 1. Clonar el repositorio
```bash
git clone https://github.com/johnalexf/ERP_COLOMBIANO_BACKEND.git
cd ERP_COLOMBIANO_BACKEND
```

### 2. Configurar el Entorno Virtual (VENV)
```bash
python -m venv venv
.\venv\Scripts\activate  # En Windows
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno (.env)
Este sistema requiere conectarse a **dos bases de datos PostgreSQL** independientes.
1. Localice el archivo `.env.templates` en la raíz del proyecto.
2. Cree una copia exacta de este archivo y renómbrela a `.env`.
3. Abra el nuevo archivo `.env` y reemplace los valores de ejemplo con sus credenciales reales de base de datos y llaves de seguridad, siguiendo las instrucciones dentro del archivo.

### 5. Sincronizar Bases de Datos
Con el archivo `.env` configurado, aplique las migraciones para construir las tablas en ambas bases de datos:
```bash
python manage.py migrate
```

### 6. Crear Acceso Administrativo
```bash
python manage.py createsuperuser
```
> **Nota:** Para detalles sobre la gestión de accesos, consulte el manual en `docs/03_Acceso_Administrativo_Django.md`.

### 7. Iniciar el Servidor
```bash
python manage.py runserver
```


---

## 📖 Documentación Interactiva (Swagger)

Una vez que el servidor esté corriendo (`python manage.py runserver`), podrá acceder al portal de pruebas y especificaciones técnicas:

* **Portal Swagger:** `http://127.0.0.1:8000/api/docs/` (Para probar los Endpoints en tiempo real).
* **Portal Redoc:** `http://127.0.0.1:8000/api/redoc/` (Documentación técnica de lectura).
* **Contrato OpenAPI:** El archivo `esquema_erp_tecnico.yml` en la raíz se puede importar en **Postman** para generar las colecciones automáticamente.

---

## 📂 Estructura del Conocimiento (`/docs`)

El proyecto cuenta con una biblioteca de manuales detallados para el mantenimiento y escalabilidad del sistema:

1. **01 al 03:** Infraestructura, Seguridad y Administración y Modelos de Usuarios Aislados (Admin/Tenant).
2. **04 al 06:** Guías de Relaciones (1:1, 1:N, M:N).
3. **07 al 10:** Auditoría SQL, Documentación automática, Protocolos de reseteo y Despliegue.

---

## 🏗️ Arquitectura de la Solución

A continuación, se detalla la arquitectura de carpetas del Backend y la función técnica de cada componente dentro del ecosistema **Django REST Framework (DRF)**.

#### A. 🧩 Capa de Dominio Aislado (`apps/`)
El sistema divide la lógica de negocio en dos "Puertas" independientes para garantizar la seguridad de los datos:
* **`apps/admin/` (Puerta 1):** Exclusivo para la gestión interna del ERP. Contiene el modelo maestro `AdminUser`.
* **`apps/tenant/` (Puerta 2):** Dedicado a los inquilinos (empresas). Aquí reside `TenantUser` y la lógica modular de negocio.

Dentro de cada dominio, se mantiene la siguiente estructura técnica:

* **`models.py` (Capa de Persistencia - CRÍTICO):** Define la estructura de datos mediante el **ORM** (Mapeo Objeto-Relacional). Actúa como la **fuente de verdad** del sistema.
    * **Mapeo:** Cada Clase de Python representa una TABLA en la base de datos.
    * **Atributos:** Cada variable (CharField, IntegerField) representa una COLUMNA.
    * **Objetos:** Cada instancia de estas clases representa una FILA de datos.
    * **Ventaja:** El ORM permite interactuar con la DB usando Python puro, evitando consultas SQL manuales y asegurando que la API reciba objetos listos para usar.

* **`serializers.py` (Capa de Serialización):** El **traductor oficial**. Convierte datos complejos del modelo (objetos de Python) a formato **JSON** para que React pueda interpretarlos, y viceversa. Aplica reglas de validación y filtra qué datos NO deben entregarse al frontend.

* **`views.py` (Capa de Control - CRÍTICO):** El motor de la API. Recibe las peticiones del Frontend, aplica las reglas de negocio, consulta los modelos y retorna los datos procesados en formato JSON.

* **`urls.py` (Enrutamiento Local):** Define las rutas específicas (Endpoints) de ese módulo (ej: `/api/admin/users/`).

* **`authentication.py` y `permissions.py` (Escudos JWT):** Motores personalizados de validación. Aseguran que un token generado en una puerta no tenga validez en la otra, manteniendo el aislamiento de sesiones.

* **`admin.py` (Gestión Interna):** Configura el panel administrativo nativo de Django para que el administrador del sistema gestione la base de datos directamente mediante una interfaz visual. No interactúa con el Frontend.

* **`migrations/` (Versionado de DB):** Historial de cambios en la estructura de la base de datos. Permite replicar o revertir cambios en el esquema SQL de manera programática.

* **`tests.py` (QA):** Archivo destinado a pruebas unitarias y de integración para asegurar la calidad y estabilidad del código.


#### **B. 🧠 Capa de Núcleo (`core/`)**
Es el centro de mando global del framework.

* **`settings.py` (Global):** Configuración maestra. Gestiona la conexión dual a PostgreSQL (Admin/Tenant), seguridad de los **Tokens (JWT)**, **políticas de CORS** y variables globales.

* **`urls.py` (Global):** Enrutador principal. Recibe todas las peticiones externas y las deriva a la Puerta 1 o Puerta 2 según corresponda. Es la entrada de la API.

* **`routers.py`:** Contiene `ErpDatabaseRouter`, que decide si una consulta va a la base de datos de administración o a la del inquilino.

* **`wsgi.py` / `asgi.py` (Despliegue):** Interfaces de puerta de enlace estándar para servidores web de producción (como IIS, AWS o DigitalOcean).


#### **C. 🛡️ Herramientas de Calidad y Seguridad**
Componentes transversales que blindan y documentan el proyecto.

* **`SimpleJWT`:** Gestión de autenticación mediante tokens de acceso y actualización para sesiones seguras, ahora configurado con aislamiento estricto.
* **`drf-spectacular`:** Generación automática de esquema OpenAPI 3.0 para documentación interactiva (Swagger).
* **CORS Headers:** Middleware encargado de permitir o restringir el acceso a la API desde dominios externos (Whitelist).

#### **D. 📂 Raíz del Proyecto**
Herramientas de ejecución, entorno y dependencias.

* **`manage.py`:** CLI (Interfaz de Línea de Comandos) de Django para tareas administrativas como correr el servidor o crear migraciones.
* **`.env` (Seguridad):** Archivo de variables de entorno. Almacena credenciales sensibles (DB passwords, Secret Keys) fuera del código fuente. **Nunca se sube al repositorio.**
* **`requirements.txt` (Dependencias):** Manifiesto de paquetes que lista todas las librerías de Python necesarias para recrear el entorno.
* **`venv/` (Aislamiento):** Directorio del Entorno Virtual. Contiene las librerías instaladas localmente para evitar conflictos globales.

---

## 🛡️ Seguridad y Blindaje de Datos

El ERP implementa múltiples capas de seguridad para garantizar la integridad y confidencialidad de la información:

### 1. Autenticación y Autorización (JWT)
* **Tokens de Acceso:** Se utiliza `SimpleJWT` para gestionar sesiones sin estado. Las peticiones a endpoints protegidos requieren la cabecera `Authorization: Bearer <token>`.
* **Aislamiento de Tokens:** Se utilizan implementaciones de `SimpleJWT` completamente separadas para `AdminUser` y `TenantUser`. Un token de administrador no funcionará para rutas de inquilino.
* **Cifrado de Contraseñas:** Django utiliza por defecto algoritmos de derivación de claves **PBKDF2** con SHA256 (estándar de la industria), asegurando que las contraseñas nunca se almacenen en texto plano.

### 2. Control de Acceso de Origen (CORS)
* **Interacción Segura:** Configuración de `django-cors-headers` para permitir peticiones exclusivamente desde dominios autorizados (Whitelist), protegiendo la API de ataques de sitios no confiables.

### 3. Integridad en Producción (Protocolo HTTPS)
* **Preparación para SSL:** El sistema cuenta con flags configurados en `settings.py` (actualmente en modo desarrollo) listos para ser activados en el despliegue final:
    * `SECURE_SSL_REDIRECT`: Redirección automática de HTTP a HTTPS.
    * `SESSION_COOKIE_SECURE` & `CSRF_COOKIE_SECURE`: Aseguran que las cookies solo se transmitan por canales cifrados.

### 4. Protección del Entorno
* **Inyección de Variables:** Uso de archivos `.env` para separar las credenciales de la base de datos y la `SECRET_KEY` del código fuente, evitando fugas de información en el repositorio.

---

## 📋 Requisitos del Sistema
* **Python:** 3.12 o superior.
* **Motor de Base de Datos:** PostgreSQL 18.
* **Arquitectura:** Windows Server 2022 (Para despliegue en IIS).

---

## 🚀 Despliegue en Producción
Esta plantilla está optimizada para la nube. Si está listo para poner su API en línea en **AWS**, consulte nuestra guía especializada:
👉 `📂 docs/10_Despliegue_ISS(AWS).md`

---

## 🛠️ Comandos de Mantenimiento Rápido
* **Actualizar dependencias:** `pip freeze > requirements.txt`
* **Limpiar archivos estáticos:** `python manage.py collectstatic`
* **Verificar integridad:** `python manage.py check`

---

© 2026 - Proyecto ERP Colombiano - Arquitectura Multi-Tenant.


