# 🚀 ERP Colombiano - Backend (Django REST Framework)

Este proyecto es el núcleo de servicios de un sistema ERP diseñado para la gestión de datos de cualquier empresa. Construido bajo una arquitectura de micro-servicios mediante una API REST blindada y documentada.

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

### 4. Configurar Variables de Entorno
1. Localice el archivo `.env.template`.
2. Cree una copia llamada `.env` en la raíz.
3. Defina sus credenciales de **PostgreSQL 18** y su `SECRET_KEY`.

### 5. Sincronizar Base de Datos
Como las migraciones ya están en el repositorio, solo aplicamos los cambios:
```bash
python manage.py migrate
```

### 6. Crear Acceso Administrativo

```bash
python manage.py createsuperuser
```

> **Nota** 
> Ver archivo ./docs/03_Acceso_Administrativo_Django.md para mayor información, en donde se debe seguir el punto 1. Creación de Superusuario (Acceso Maestro) y saltarse al paso 3. Protocolo de Validación y Puesta en Marcha.
> Se ignora el paso 2 puesto que las configuraciones ya se realizaron.

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

1. **01 al 03:** Infraestructura, Seguridad y Administración.
2. **04 al 06:** Guías de Relaciones (1:1, 1:N, M:N).
3. **07 al 09:** Auditoría SQL, Documentación y Protocolos de Reseteo.

---

## 🏗️ Arquitectura de la Solución

A continuación, se detalla la arquitectura de carpetas del Backend y la función técnica de cada componente dentro del ecosistema **Django REST Framework (DRF)**.

#### A. 🧩 Capa de Aplicación (`apps/`)
Contiene la lógica de negocio dividida por dominios (Usuarios, Inventario, otras funciones..). Es el núcleo funcional del ERP.

* **`models.py` (Capa de Persistencia - CRÍTICO):** Define la estructura de datos mediante el **ORM** (Mapeo Objeto-Relacional). Actúa como la **fuente de verdad** del sistema.
    * **Mapeo:** Cada Clase de Python representa una TABLA en la base de datos.
    * **Atributos:** Cada variable (CharField, IntegerField) representa una COLUMNA.
    * **Objetos:** Cada instancia de estas clases representa una FILA de datos.
    * **Ventaja:** El ORM permite interactuar con la DB usando Python puro, evitando consultas SQL manuales y asegurando que la API reciba objetos listos para usar.

* **`serializers.py` (Capa de Serialización):** El **traductor oficial**. Convierte datos complejos del modelo (objetos de Python) a formato **JSON** para que React pueda interpretarlos, y viceversa, aplicando reglas de validación de datos, además tambien permite ser un filtro de que datos no tienen que ser entregados al frontend.

* **`views.py` (Capa de Control - CRÍTICO):** El motor de la API. Recibe las peticiones del Frontend, aplica las reglas de negocio, consulta los modelos y retorna los datos procesados en formato JSON.

* **`urls.py` (Enrutamiento Local):** Define las rutas específicas (Endpoints) de este módulo (ej: `/api/users/`).

* **`admin.py` (Gestión Interna):** Configura el panel administrativo nativo de Django para que el administrador del sistema gestione la base de datos directamente mediante una interfaz visual. No interactúa con el Frontend.

* **`migrations/` (Versionado de DB):** Historial de cambios en la estructura de la base de datos. Permite replicar o revertir cambios en el esquema SQL de manera programática.

* **`tests.py` (QA):** Archivo destinado a pruebas unitarias y de integración para asegurar la calidad y estabilidad del código.

* **`backends.py` (Lógica de Autenticación Híbrida):**  Es el "Portero Inteligente" del sistema. Por defecto, Django solo sabe reconocer a los usuarios por su `username`. Este archivo contiene una clase personalizada que expande esa capacidad, permitiendo que el sistema valide credenciales tanto por **correo electrónico** como por **nombre de usuario**.


#### **B. 🧠 Capa de Núcleo (`core/`)**
Es el centro de mando global del framework.

* **`settings.py` (Global):** Configuración maestra. Gestiona la conexión a PostgreSQL, seguridad de los **Tokens (JWT)**, aplicaciones instaladas, **políticas de CORS** y variables globales.
* **`urls.py` (Global):** Enrutador principal. Recibe todas las peticiones externas y las deriva a la aplicación correspondiente dentro de `apps/`. Es la puerta de entrada de la API.
* **`wsgi.py` / `asgi.py` (Despliegue):** Interfaces de puerta de enlace estándar para servidores web de producción (como IIS, AWS o DigitalOcean).

#### **C. 🛡️ Herramientas de Calidad y Seguridad**
Componentes transversales que blindan y documentan el proyecto.

* **`SimpleJWT`:** Gestión de autenticación mediante tokens de acceso y actualización para sesiones seguras.
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
Para garantizar la estabilidad de la "Torre de Control", asegúrese de contar con:
* **Python:** 3.12 o superior.
* **Motor de Base de Datos:** PostgreSQL 18.
* **Arquitectura:** Windows Server 2022 (Para despliegue en IIS).

---

## 🚀 Despliegue en Producción
Esta plantilla está optimizada para la nube. Si está listo para poner su API en línea en **AWS**, consulte nuestra guía especializada:
👉 `📂 docs/11_Despliegue_ISS(AWS).md`

---

## 🛠️ Comandos de Mantenimiento Rápido
* **Actualizar dependencias:** `pip freeze > requirements.txt`
* **Limpiar archivos estáticos:** `python manage.py collectstatic`
* **Verificar integridad:** `python manage.py check`

---

© 2026 - Proyecto ERP Colombiano - Desarrollo Profesional.


