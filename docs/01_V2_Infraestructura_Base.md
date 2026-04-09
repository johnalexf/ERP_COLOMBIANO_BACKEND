# 🚀 Manual de Configuración: Backend API REST (ERP Colombiano) 

Este documento constituye el cimiento técnico del ERP. Cubre desde la preparación del entorno lógico hasta la interconexión con el motor de base de datos PostgreSQL, garantizando una arquitectura de seguridad desacoplada (Headless) y Multi-Tenant preparada para ser consumida por el Frontend.

Al finalizar esta guía, el sistema contará con una "Torre de Control" configurada, un puente de comunicación (CORS) establecido, un enrutamiento estricto de bases de datos y la capacidad de gestionar variables de entorno sensibles mediante estándares industriales.

---

## 1. 🐍 Instalación de Python
Se requiere la interpretación del lenguaje en su versión más reciente para asegurar la compatibilidad con las librerías modernas.

```bash
# 1. Descargar e instalar Python (Versión recomendada 3.12 o superior) desde: [https://www.python.org/downloads/](https://www.python.org/downloads/)
# 2. Reiniciar el equipo para refrescar las variables de entorno del sistema.
# 3. Verificar la versión instalada en la terminal:
python --version
```

---

## 2. 📂 Navegación y Directorios
Comandos básicos para ubicar la ruta del proyecto y preparar la estructura de carpetas de forma organizada.

Instrucciones para ubicar la carpeta del proyecto mediante la línea de comandos (CMD).

```bash
# Listar archivos y carpetas en la ubicación actual
dir

# Navegar a una ruta específica (Ejemplo: Ir a Documentos)
# El flag /d asegura el cambio de unidad si es necesario.
cd /d "ruta_de_la_carpeta"

# Crear la carpeta del servidor
mkdir backend

# Ingresar a la carpeta creada
cd backend
```

---

## 3. 📦 Entorno Virtual (Virtual Env)
Creación de un contenedor aislado para las librerías, evitando conflictos con otros proyectos. Es el equivalente funcional de `node_modules` en otros entornos. 
Funciona como un compartimento hermético (`venv`) que aloja una copia local de Python para mantener las dependencias bajo control.

> [!IMPORTANT]
> **Ejecutar CMD como administrador:** 
> Se recomienda ejecutar el siguiente comando en una terminal con permisos suficientes para asegurar que Python pueda crear la estructura de archivos sin restricciones del sistema.

```bash
# Ejecutar dentro de la carpeta 'backend' con CMD o PowerShell como administrador:
python -m venv venv
```

---

## 4. ⚡ Activación del Entorno (Estado Crítico)
Este paso es **obligatorio** antes de **instalar librerías** o **ejecutar el servidor**. Habilita el uso de las dependencias aisladas.
Desde aquí ya no es necesario estar como administrador en la terminal, se puede desde powerShell o la terminal integrada de Visual.

```bash
# Comando de activación para Windows:

# Desde CMD (Símbolo del sistema)
\venv\Scripts\activate

# PowerShell o terminal integrada de Visual Studio Code
.\venv\Scripts\activate
```

> [!WARNING]
> **Verificación:** Al inicio de la línea de comandos debe aparecer el indicador `(venv)`.
> * Correcto: `(venv) C:\Ruta\backend>`
> * Incorrecto: `C:\Ruta\backend>` (Si no aparece, repetir el comando por que el entorno no está activo).


---
## 5. 🧱 Instalación de Componentes (Dependencias)
Descarga de los frameworks y herramientas necesarias para la comunicación con el Frontend, la Base de Datos y la Seguridad de grado empresarial mediante JWT puro.

**Lista de paquetes principales:**
* `django`: El chasis o estructura principal del proyecto.
* `djangorestframework`: El motor para construir la Web API.
* `django-cors-headers`: El puente de comunicación segura entre React y Django.
* `psycopg2-binary`: La tubería de conexión para PostgreSQL.
* `python-decouple`: La caja fuerte para gestionar llaves y contraseñas mediante archivos `.env`.
* `djangorestframework-simplejwt`: Único y verdadero motor de seguridad. Estándar para el manejo de llaves digitales (Tokens) con expiración.
* `drf-spectacular`: Generación de documentación técnica interactiva (Swagger/Redoc).

```bash
# Instalación masiva de componentes:
pip install django djangorestframework django-cors-headers psycopg2-binary python-decouple djangorestframework-simplejwt drf-spectacular
```

### 🔐 Nota sobre Seguridad "Http-Only & Secure"
Se integra la librería `djangorestframework-simplejwt` desde el inicio para que la arquitectura soporte niveles de protección avanzados:
1. **Cookies Http-Only:** Actúan como un sobre sellado que impide que atacantes roben la sesión mediante scripts maliciosos (XSS).
2. **Bandera Secure:** Asegura que los datos solo viajen por túneles encriptados (HTTPS).

> **Aviso Técnico:** Durante las pruebas por IP (HTTP), las funciones de "Secure" se mantendrán desactivadas en el archivo `.env` para evitar bloqueos del navegador, pero el código ya estará listo para activarlas con un solo cambio de variable al pasar a producción final con direccion https para el servidor.


---

## 6. 🧠 Inicialización del Núcleo (Core)
Se genera la estructura de configuración global. Se utiliza el nombre `core` por convención para identificar los archivos de configuración.
Generación de la "Torre de Control" del proyecto. Contiene los archivos `settings.py` y `urls.py`.

> **Importante:** El punto `.` al final del comando es vital para evitar la creación de subcarpetas redundantes.

```bash
django-admin startproject core .
```

---

## 7. 📁 Estructura de Aplicaciones (Apps)
Organización modular del sistema. Aquí se alojarán los módulos divididos por dominios lógicos y de base de datos: el Administrativo (`admin`) y el de Inquilinos (`tenant`). 

```bash
# 1. Crear directorio principal de aplicaciones:
mkdir apps
cd apps

# 2. Crear los subdominios:
mkdir admin tenant

# Django requiere una estructura específica para manejar cada funcionalidad de forma independiente.
# 3. Crear la App administrativa dentro de su dominio:
cd admin
django-admin startapp admin_users
cd ..

# 4. Crear la App de inquilinos dentro de su dominio:
cd tenant
django-admin startapp tenant_users

# 5. Regresar a la raíz del proyecto:
cd ../..
```

---

## 8. 📜 Registro de Requerimientos (Requirements)
Generación del archivo de control de versiones de las librerías para garantizar que cualquier equipo de trabajo utilice exactamente las mismas herramientas.

```bash
# Exportar lista de dependencias:
pip freeze > requirements.txt
```

---

## 9. 🗄️ Configuración de PostgreSQL
Antes de que Django pueda gestionar datos, se debe preparar el motor de base de datos profesional en PostgreSQL 18.

1. **Descarga:** Instalar PostgreSQL (Versión 18) desde el sitio oficial. [PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
2. **Clave de Acceso:** Registrar la contraseña definida durante la instalación; se requerirá para la conexión con Django.
3. **Creación de la Base de Datos (pgAdmin 4):**
   * Abrir pgAdmin 4 y conectarse al servidor local.
   * Clic derecho en `Databases` > `Create` > `Database...`
   * Crear la primera base: `erp_admin_bd` (Para el núcleo y dueños del sistema).
   * Crear la segunda base: `erp_tenant_bd` (Para los clientes e inquilinos).
   * Estos nombre debe coincidir con el valor configurado en el archivo `.env`.

---

## 10. 🔐 Gestión de Variables de Entorno (.env)
Para proteger la integridad de la empresa, las credenciales sensibles se almacenan en un archivo independiente que **nunca** debe subirse al repositorio público.

**Llaves del proyecto**
* `DEBUG=True`: Modo desarrollador; 
True para mostrar exactamente donde paso el error; 
False solo muestra "Error 500 - Algo salió mal", sin detalles.
**Poner en False en produccion.**
* `SECRET_KEY=clave_aleatoria_super_secreta`: Clave para encriptar datos importantes como tokens.
* `ALLOWED_HOSTS=127.0.0.1,localhost,IP_DEL_SERVIDOR`: Django Solo responde si la petición viene dirigida a estos nombres.

* `DB_NAME_DEFAULT=erp_admin_bd`
* `DB_USER=postgres`
* `DB_PASSWORD=contraseña`
* `DB_HOST=localhost` : Direccion de la base de datos
* `DB_PORT=5432` : 5432 es el puerto estándar de Postgres

* `DB_NAME_TENANT=erp_tenant_db`
* `DB_USER_TENANT=usuario`
* `DB_PASSWORD_TENANT=contraseña`
* `DB_HOST_TENANT=localhost` : Direccion de la base de datos
* `DB_PORT_TENANT=5432` : 5432 es el puerto estándar de Postgres

* `CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://IP_DEL_SERVIDOR:3000` : El "permiso de fronteras". Permite que el navegador acepte datos enviados desde el puerto de React hacia el de Django.
* `USE_HTTPS=False` : Interruptor Maestro. Controla si Django exige túneles seguros y cookies blindadas, False (Evita bloqueos en pruebas).


```bash
# Desde visual studio code
# 1. Crear un archivo llamado exactamente '.env' en la carpeta raíz (donde está el manage.py).
# 2. Agregar el siguiente contenido base (ajustar con datos reales):
# NO espacios alrededor del signo =

# ----------------- CONFIGURACIÓN DEL PROYECTO -----------------------------
DEBUG=True
SECRET_KEY=cambiar_por_una_llave_muy_larga_y_compleja
ALLOWED_HOSTS=127.0.0.1,localhost,IP_DEL_SERVIDOR

# ------------ CONEXIÓN A BASES DE DATOS (Multi-Tenant) -------------------

# --- CONEXIÓN A BASE DE DATOS ADMIN (DEFAULT) ---
DB_NAME_DEFAULT=erp_admin_db
DB_USER=postgres
DB_PASSWORD=104862
DB_HOST=localhost
DB_PORT=5432

# --- CONEXIÓN A BASE DE DATOS INQUILINOS (TENANT) ---
DB_NAME_TENANT=erp_tenant_db
DB_USER_TENANT=postgres
DB_PASSWORD_TENANT=104862
DB_HOST_TENANT=localhost
DB_PORT_TENANT=5432

# --------------------- SEGURIDAD DE RED (CORS) -------------------------
# Define el origen permitido para las peticiones de React.
# Sin espacios después de la coma
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://IP_DEL_SERVIDOR

# --------------- INTERRUPTORES DE SEGURIDAD (SSL/COOKIES) ---------------
# False para pruebas locales por IP. True para producción con HTTPS.
USE_HTTPS=False

```

---

## 11. Configurar el Cerebro (settings.py)

En este paso vinculamos las variables de entorno con la lógica de Django. No se debe borrar todo el archivo; se deben buscar estas secciones y actualizarlas en `core/settings.py`, o si es el caso crearlas.


### A.🗄️ Configuración de .env como variables dentro de settings.py y Seguridad Dinámica
Vincular el motor de Python con el archivo de configuración externa y preparar los interruptores de seguridad.`python-decouple`.

* **Al inicio del archivo:** Importar `config` (Librería de lectura) y `Csv` para manejar listas (como las IPs de CORS).


```Python
from pathlib import Path
from decouple import config, Csv  # <--- AGREGAR ESTA LÍNEA (Es vital)

#Config Sirve para que la aplicación pueda leer las variables del archivo .env y usarlas dentro de este mismo archivo (settings.py).

# Interruptor Maestro de Seguridad (Viene del .env)
# Si es False, permite pruebas por IP/HTTP. Si es True, exige HTTPS.
USE_HTTPS = config('USE_HTTPS', default=False, cast=bool)
```

* **Buscar SECRET_KEY, DEBUG y ALLOWED_HOSTS:**

```python
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# Lee las IPs del .env y las convierte en una lista automáticamente
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())
```

---

### B. 🧠 Registro de Módulos, Seguridad (CORS) y Autenticación (JWT)
Configurar el "Cerebro" del sistema para que reconozca las nuevas herramientas instaladas y permita la conexión con la pagina web.

* **Modificar INSTALLED_APPS:**

```python
INSTALLED_APPS = [
    # ... aplicaciones por defecto de django ...

    # ... otras aplicaciones ...
    'drf_spectacular',

    # --- TERCEROS ---
    'rest_framework',
    # 'rest_framework.authtoken',  # Requerida por dj-rest-auth / authotoken => tokens opacos
    # 'dj_rest_auth',              # Gestionar autenticacion / login genérico que requería authtoken
    # 'rest_framework.authtoken' y 'dj_rest_auth' no se va utilizar porque la arquitectura evolucionó a JWT puro y "Dos Puertas" separadas.
    'rest_framework_simplejwt',  # Seguridad JWT
    'corsheaders',               # Permisos de conexión (CORS)
    
    # --- APPS ---
    # --- DOMINIO ADMINISTRATIVO ---
    'apps.admin.admin_users',
    
    # --- DOMINIO INQUILINOS (NEGOCIO) ---
    'apps.tenant.tenant_users',
]
```

* **Buscar MIDDLEWARE y agregar el CorsMiddleware (¡De primero!):**

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # <--- ESTE VA DE PRIMERO
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ... resto de middlewares ...
]
```

* **Definición del Estándar de Autenticación:**
Configurar el comportamiento de Django Rest Framework. Copiar y pegar al **final del archivo**.

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

> **Nota Técnica:** 
> El bloque `REST_FRAMEWORK` establece la **JWTAuthentication** como el estándar global del sistema. Esto permite que el servidor sea "stateless" (sin estado), delegando la validación de identidad a tokens encriptados, lo cual es ideal para la integración con React.

#### Actualización de Ruta en las Apps
Ajustar los archivos `apps.py` de cada aplicación para mantener la coherencia con la estructura de carpetas modular.

Para `apps/admin/admin_users/apps.py`:
```Python
from django.apps import AppConfig

class AdminUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.admin.admin_users'  # Ruta física exacta (donde está la carpeta)
    label = 'admin_users'            # Nombre interno para el router
    # El 'label' es el nombre corto interno (direccion logica para evitar problemas con la búsqueda desde el núcleo hasta la app)
```

Para `apps/tenant/tenant_users/apps.py`:
```Python
from django.apps import AppConfig

class TenantUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tenant.tenant_users'
    label = 'tenant_users'
```

Es necesario para mantener una concordancia de la direccion configurada en core/settings.py

> **Nota de Arquitectura:**
> Al usar la carpeta `apps/` y las subcarpetas `apps/admin` y `apps/tenant` para organizar el proyecto, es obligatorio definir `label = 'admin_users'` y  `label = 'tenant_users'` en el `apps.py` de cada modelo. Esto permite que el sistema reconozca la app con un nombre corto y limpio, facilitando la conexión con cada modelo de usuario (`admin_users.AdminUser`) y (`tenant_users.TenantUserUser`) manteniendo las tablas de PostgreSQL organizadas.


### C. 🛡️ Blindaje y Permisos (CORS e HTTPS)
Define las reglas de visibilidad del servidor y los protocolos de seguridad para el tráfico de datos global.

* **Al final del archivo: (settings.py)**  (Abajo del todo), dar permiso explícito a la página web tanto los CORS como las Cookies:

* **Configuración de CORS (Lectura desde .env):**
Permite que el Frontend (React) se comunique con el Backend. Sin esto, el navegador bloqueará las peticiones por seguridad.

```python
# Permite que el navegador acepte datos de las IPs o Urls listadas en el .env
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv())
```

* **Configuración de Seguridad SSL/Cookies:**
Estas reglas aseguran que la información viaje encriptada y protegen las sesiones del servidor. Estas líneas usan el valor de `USE_HTTPS` que se definió al inicio.

```python
# Seguridad de Cookies y Red
SESSION_COOKIE_HTTPONLY = True  # Protege contra robo de sesión por JS (XSS)
SESSION_COOKIE_SECURE = USE_HTTPS # Las cookies de sesión solo viajan por canales seguros (HTTPS)
CSRF_COOKIE_SECURE = USE_HTTPS  # Protege los formularios contra ataques de falsificación
SECURE_SSL_REDIRECT = USE_HTTPS  # Redirige automáticamente HTTP a HTTPS si es True
```

> **Nota:**
> Aun que `USE_HTTPS` esta en estado `FALSE` se dejan las configuraciones listas para cuando las pruebas en el servidor ya tengan un dominio.


### D. 🔑 Reglas de Vigencia de Tokens (SimpleJWT)

Establece la duración de las credenciales digitales para equilibrar la seguridad con la comodidad del flujo de trabajo.

Este bloque va al final del archivo `core/settings.py`. 

```python
from datetime import timedelta # <--- Necesario para medir tiempos

# --- CONFIGURACIÓN DE TOKENS (SimpleJWT) ---
# Define el comportamiento y duración de las llaves digitales para la API.
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # El carnet de acceso dura 1 hora
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # La llave de repuesto dura 1 día
    'ROTATE_REFRESH_TOKENS': True,                  # Genera una nueva llave maestra cada vez que se usa
    'ALGORITHM': 'HS256',                           # Algoritmo estándar de cifrado
    'SIGNING_KEY': SECRET_KEY,                      # Firma los tokens con la llave secreta del proyecto
    'AUTH_HEADER_TYPES': ('Bearer',),               # Prefijo que exigirá Postman/React: 'Bearer <token>'
}
```


### E. 🗄️ Conexión a Base de Datos Profesional
Sustituir la configuración de SQLite por PostgreSQL separando los dominios de datos.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME_DEFAULT'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    },
    'tenant': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME_TENANT'),
        'USER': config('DB_USER_TENANT', default=config('DB_USER')), 
        'PASSWORD': config('DB_PASSWORD_TENANT', default=config('DB_PASSWORD')),
        'HOST': config('DB_HOST_TENANT', default=config('DB_HOST')),
        'PORT': config('DB_PORT_TENANT', default=config('DB_PORT')),
    }
}

# Enrutador de tráfico para separar la data administrativa de la del negocio
DATABASE_ROUTERS = ['core.routers.ErpDatabaseRouter']
```

> **Aviso Crítico:** Antes de realizar las migraciones (`python manage.py migrate`), se debe crear el archivo `core/routers.py` con la clase `ErpDatabaseRouter` para que Django sepa a qué base de datos enviar cada tabla.

## 12. 🚦 Creación del Enrutador Estricto (Multi-Tenant)

Para que la arquitectura de "Dos Puertas" funcione, Django necesita un archivo de reglas estrictas que le indique hacia qué base de datos debe enviar la información de cada aplicación. Si este archivo no existe, el sistema fallará al intentar arrancar.

Crear el Archivo: `core/routers.py` (En la misma carpeta donde está `settings.py`)

```python

class ErpDatabaseRouter:
    """
    Enrutador principal ESTRICTO (Strict Allowlist) para la arquitectura Multi-Tenant.
    Controla el tráfico entre la base de datos administrativa y la de inquilinos.
    No permite ambigüedades. Toda aplicación debe estar declarada explícitamente.
    """
    
    # 1. Apps que viven en la base de datos de los clientes inquilinos (empresas)
    TENANT_APPS = ['tenant_users']

    # 2. Apps que viven en la base de datos central administrativa
    # aplicaciones (nativas y nuestras) que van a la base administrativa
    # Incluimos las apps internas de Django para que no se pierdan
    ADMIN_APPS = [
        'admin_users', 
        'admin', 
        'auth', 
        'contenttypes', 
        'sessions',
    ]

    def _get_db(self, app_label):
        """
        Motor de decisión central con Fallo Rápido (Fail-Fast).
        Si un programador instala una librería y no la declara aquí, estalla.
        """
        if app_label in self.TENANT_APPS:
            return 'tenant'
        elif app_label in self.ADMIN_APPS:
            return 'default'
        else:
            # Cero ignorancia. Error forzado.
            raise ValueError(f"¡ALERTA ARQUITECTÓNICA! La aplicación '{app_label}' está intentando acceder a la base de datos, pero no ha sido declarada en las listas del ErpDatabaseRouter.")


    def db_for_read(self, model, **hints):
        """ FIN: Decidir de dónde traer la información (Lectura). """
        return self._get_db(model._meta.app_label)

    def db_for_write(self, model, **hints):
        """
        FIN: Decidir dónde guardar la información (Escritura).
        Asegura que si se crea un administrador, se guarde en la DB central, 
        y si se crea un usuario de negocio, se guarde en la DB del cliente.
        """
        return self._get_db(model._meta.app_label)

    def allow_relation(self, obj1, obj2, **hints):
        """
        FIN: Blindaje de integridad.
        Su fin es prohibir que una tabla de 'Negocio' intente amarrarse físicamente
        a una tabla de 'Administración'. Esto evita errores catastróficos.
        Solo permite relaciones si AMBOS modelos pertenecen a la misma base de datos.
        """
        db1 = self._get_db(obj1._meta.app_label)
        db2 = self._get_db(obj2._meta.app_label)
        return db1 == db2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        FIN: Constructor de infraestructura.
        Cuando se ejecuta el comando 'migrate', esta función le dice a Django:
        'Crea estas tablas SÓLO en esta base de datos'. 
        Evita que la tabla de Usuarios Administrativos aparezca por error en la DB del Cliente.
        """
        expected_db = self._get_db(app_label)
        return db == expected_db

```

---

## 13. 🧪 Prueba de Fuego

Una vez guardados los cambios en `settings.py` y se tenga el archivo `.env` listo, Asegúrar de que la base de datos en PostgreSQL exista.

En la terminal (con (venv) activo), ejecutar:

```Bash
python manage.py check
```
> **Resultado esperado:** `System check identified no issues (0 silenced).`
> Django se puede conectar a PostgreSQL y esta listo para crear las tablas. Esto no significa que se haya establecido una conexion continua, solo es una prueba de verificacion de conexion.

> Si sale un `error de psycopg2`, probablemente es porque PostgreSQL no está corriendo en los servicios de Windows.

---


## 14. 🛡️ Control de Versiones (.gitignore)

El archivo `.gitignore` es fundamental para mantener el repositorio limpio y seguro. Evita que archivos temporales, configuraciones personales o datos sensibles (como contraseñas) suban al servidor o se compartan con otros desarrolladores.

### Contenido del archivo `.gitignore`
Crear un archivo llamado exactamente `.gitignore` en la raíz del proyecto (al mismo nivel que `manage.py`):

```bash
# --- PYTHON ---
# Archivos de código compilado por Python.
__pycache__/     
# Archivos compilados individuales.
*.py[cod]       

# --- ENTORNO VIRTUAL ---
# El contenedor de librerías (pesado y específico de cada PC).
env/
venv/      
# ¡CRÍTICO! Contiene contraseñas y llaves de seguridad.
.env             
# --- BASE DE DATOS LOCAL ---
# Base de datos de prueba (No subir a producción).
*.sqlite3 

# --- EDITORES Y SISTEMA ---
# Configuraciones personales de Visual Studio Code.
.vscode/  
# Configuraciones de PyCharm.        
.idea/  
# Archivos temporales de sistema (macOS).          
.DS_Store 

web.config
static/
```

### 🧠 Justificación Técnica: ¿Por qué ignoramos estos archivos?

| Elemento | Razón Técnica |
| :--- | :--- |
| **`__pycache__/`** | Contiene el código procesado para que Python corra más rápido. Es específico del procesador y sistema operativo; no tiene sentido compartirlo. |
| **`venv/`** | Es el "contenedor" de librerías. Puede pesar cientos de MB y se recrea fácilmente con el comando `pip install -r requirements.txt`. |
| **`.env`** | Es la **Llave Maestra**. Aquí se guarda la contraseña de PostgreSQL y el `SECRET_KEY` de Django. Si se sube al repo, cualquiera podría hackear el sistema. |
| **`*.sqlite3`** | Cuando se hacen pruebas locales rápidas, Django crea este archivo. Contiene datos de prueba que no deben mezclarse con la base de datos real del ERP. |
| **`.vscode/`** | Guarda preferencias personales (color del tema, tamaño de letra). Otro desarrollador puede tener gustos distintos y no queremos sobreescribir sus ajustes. |


---

## 15. 🏗️ Preparación para Producción (Static Files)
A diferencia de React, Django no se "compila", pero sus archivos estáticos (CSS, JavaScript del Admin, Imágenes) deben agruparse en una carpeta única para que el servidor web (IIS o Nginx) pueda servirlos eficientemente.

### Configuración en core/settings.py

Buscar :

```Python
# URL para acceder a los archivos desde el navegador
STATIC_URL = '/static/'
```

Y Agregar:

```Python
import os

# Carpeta física donde se recolectarán todos los archivos (Ruta absoluta)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```


---
© 2026 - Proyecto ERP Colombiano - Desarrollo Profesional.