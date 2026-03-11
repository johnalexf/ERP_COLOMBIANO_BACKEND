# 👤 Implementación de Modelo de Usuario Personalizado (Custom User)

Este manual describe el procedimiento para sustituir el modelo de autenticación por defecto de Django por uno personalizado. Este paso es fundamental para permitir que el sistema almacene información específica (Cédula, NIT, Empresa) manteniendo la seguridad nativa del framework. Además, incluye los pasos para activar los puntos de acceso (Endpoints) con la lógica de negocio.

---


## 1. Definición del Modelo
Se debe modificar el archivo `apps/users/models.py`. La estructura del modelo debe incluir los campos requeridos para el contexto empresarial.

### Justificación Técnica: AbstractUser
Se utiliza `AbstractUser` para heredar la gestión de sesiones y la encriptación de contraseñas (Hashing) de Django. Esto funciona como un **"archivo maestro de identidad"** que ya sabe cómo guardar llaves de forma segura, permitiendo agregar solamente los atributos adicionales que el ERP necesita.

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Extensión del modelo de usuario estándar para el ERP.
    Hereda: username, password, email, first_name, last_name.
    """

    email = models.EmailField(unique=True)

    cedula = models.CharField(max_length=20, unique=True, verbose_name="Cédula o NIT")
    telefono = models.CharField(max_length=15, blank=True, null=True)
    cargo = models.CharField(max_length=50, blank=True, null=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.cedula}"
```

> **Representación Legible (`__str__`):**
>  Este método define cómo se identifica a un usuario dentro del sistema en interfaces visuales (como el Panel de Administración). En lugar de mostrar un código genérico `User object (1)`, el sistema devolverá una cadena clara como `john_doe - 1012345678`, lo cual  facilita la auditoría visual y la búsqueda de registros específicos sin necesidad de entrar al detalle de cada perfil.

---

## 2. Configuración del Núcleo (Settings)
Para que el motor de Django reconozca el nuevo modelo como el sistema de autenticación global, es obligatorio registrarlo en el archivo `core/settings.py`.

```python
# Al final del archivo core/settings.py:
AUTH_USER_MODEL = 'users.User'
# Django busca la app con label 'users' y dentro de él el modelo 'User'
```
**Nota:** Esta configuración debe realizarse antes de ejecutar cualquier migración inicial para evitar conflictos de integridad en la base de datos.


### 2.1. Configuración de Autenticación Híbrida (Allauth)
Para que el sistema sea flexible y permita al usuario iniciar sesión con su **Correo Electrónico** o su **Nombre de Usuario**, ajustamos el comportamiento de `django-allauth` en `core/settings.py`.

```python
# Configuraciones adicionales en core/settings.py:

# --- CONFIGURACIÓN DE AUTENTICACIÓN AVANZADA ---

# Método de autenticación: 'username_email' permite AMBOS.
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  

# El correo es obligatorio y no se puede repetir en la base de datos.
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

# El username sigue siendo requerido para la base de datos interna
ACCOUNT_USERNAME_REQUIRED = True 

# Evita que pida confirmación de email por correo (útil para pruebas locales).
# Se activa cuando se haya configurado un servidor de correos (SMTP).
ACCOUNT_EMAIL_VERIFICATION = 'none'
```

> [!NOTE]
> **Lógica de Autenticación:** 
> Al usar `'username_email'`, el sistema detecta automáticamente si lo que escribió el usuario tiene un `@`. Si lo tiene, busca por correo; si no, busca por nombre de usuario. Es la opción más versátil.

> **Restricción Técnica:**
> Para evitar colisiones en el inicio de sesión híbrido, el campo `username` no debe permitir el carácter `@`. De esta forma, el sistema puede distinguir inequívocamente entre un correo y un alias de usuario.

> **Diferencia Técnica:**
> * `django-allauth`: Es el motor lógico (valida correos, unicidad y procesos de cuenta).
> * `dj-rest-auth`: Es la interfaz (convierte la lógica anterior en URLs tipo JSON para React).

---

---

## 3. Persistencia en Base de Datos (PostgreSQL)
Una vez definido el modelo y su ruta en la configuración, se procede a la creación física de las tablas en PostgreSQL 18.

1. **Activación del Entorno (Estado Crítico)**
    ```bash
    # Comando de activación para Windows:
    .\venv\Scripts\activate
    # Siempre se debe verificar la presencia del indicador (venv) en la terminal antes de ejecutar cualquier comando python manage.py.
    ```

2. **Verificar prueba de conexión a la base de datos**
    ```Bash
    python manage.py check
    # RESULTADO ESPERADO: 
    # System check identified no issues (0 silenced)".
    ```

3. **Generación del archivo de migración:**
   Este comando analiza el código Python y genera un archivo de instrucciones técnicas en python que Django entiende donde se registran cambios en las tablas.
   ```bash
   python manage.py makemigrations users
   ```

4. **Aplicación de cambios:**
   Este comando ejecuta las instrucciones en el servidor de base de datos.
   ```bash
   python manage.py migrate
   ```

---
 

# 🔌 Conectividad con React
Como los usuarios son la puerta de entrada al ERP, necesitamos definir cómo se "traducen" estos datos para que viajen de la base de datos al Frontend.

## 4. Serialización: Traducción de Datos a JSON
El serializador actúa como un filtro de seguridad y validación. Transforma los objetos de la base de datos en JSON para **React** y viceversa. 
Cuando se van a guardar los datos en la base de datos, despues de estar confirmados y validados el serializador le da la orden al ORM de django-rest que guarde los datos.

Incluye el metodo que rebota contraseñas débiles y asegura que el ORM encripte la clave antes de guardarla.

**Crear el Archivo:** `apps/users/serializers.py`

```python
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password # <--- Filtro de seguridad de Django
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Heredar de ModelSerializer otorga automáticamente las funciones de:
    LECTURA (List/Retrieve), EDICIÓN (Update/Patch) y ELIMINACIÓN (Delete).
    """

    # Definimos password como "solo escritura" (no se muestra en los GET)
    # Configuración de seguridad: React envía la clave (write), 
    # pero Django nunca la devuelve en el JSON de respuesta (read).
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        # Define el modelo de origen de los datos.
        model = User 
        
        # Lista blanca de campos que el serializador manejará.
        fields = ['id', 'username', 'password', 'email', 'cedula', 'telefono', 'cargo', 'empresa']

    # --- VALIDACIÓN DE CONTRASEÑA ---
    def validate_password(self, value):
        """
        Ejecuta los validadores de Django (longitud, claves comunes, etc.).
        Si la clave es débil (ej. '123'), lanzará un error 400 automáticamente.
        """
        validate_password(value)
        return value

    def create(self, validated_data):
        """
        Sobrescritura del método de creación para forzar la encriptación.
        .create_user: Método especial de Django que aplica Hashing a la contraseña.
        """
        user = User.objects.create_user(**validated_data)
        return user
```

> [!IMPORTANT]
> **Notas de Arquitectura:**
> 1. **CRUD Integrado:** Al usar `ModelSerializer`, ya tienes incluido internamente el método `.update()` para editar usuarios y el mapeo para borrarlos. No necesitas escribirlos manualmente.
> 2. **Login vs Registro:** Este serializador es para gestionar los datos del perfil y registros nuevos (CRUD). El **Inicio de Sesión** lo gestiona la librería `dj-rest-auth`, que ya trae sus propios serializadores para validar credenciales y entregar Tokens JWT.


#### 🛡️ Validadores de Seguridad de Contraseña (Sensores)
Al invocar `validate_password(value)`, Django activa 4 filtros estándar definidos en el núcleo del sistema (`AUTH_PASSWORD_VALIDATORS`):

* **Similitud:** La clave no puede parecerse al nombre de usuario o al email (ej: no puede ser `john123`).
* **Longitud Mínima:** El estándar de seguridad exige al menos **8 caracteres**.
* **Contraseña Común:** El sistema rebota la clave si está en la lista de las 1,000 más usadas (ej: `password123`, `12345678`).
* **No Numérica:** No se permiten claves compuestas exclusivamente por números (ej: `123456789`).


---


### 5. Lógica de la API (Views)
La Vista es el centro de mando que coordina al Modelo y al Serializador para responder a las peticiones de la red que son redirigidas desde la urls.py hacia esta vista.

**Archivo:** `apps/users/views.py`

```python
from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated 
# Importa el nivel de acceso permitido, 
# AllowAny (Acceso a todo mundo) 
# IsAuthenticated (Acceso con token)
from .models import User
from .serializers import UserSerializer

# True para desarrollo, False para producción
MODO_PRUEBAS = settings.DEBUG

class UserViewSet(viewsets.ModelViewSet):
# viewsets.ModelViewSet: Clase maestra que ya incluye la lógica para Listar, Crear, Ver, Editar y Borrar.
    """
    ModelViewSet concentra en una sola clase las 5 acciones del CRUD:
    - Listar (GET /)
    - Crear (POST /)
    - Ver detalle (GET /id/)
    - Editar (PUT-PATCH /id/)
    - Borrar (DELETE /id/)
    """
    queryset = User.objects.all() 
    # queryset: Define la consulta a la base de datos (En este caso, traer todos los usuarios).

    serializer_class = UserSerializer 
    # serializer_class: Especifica qué "traductor" JSON usará esta vista.

    permission_classes = [AllowAny] if MODO_PRUEBAS else [IsAuthenticated]
    # permission_classes: Define el protocolo de seguridad. AllowAny abre la puerta para pruebas iniciales.
```

> [!TIP]
> **¿Por qué usamos ModelViewSet?**
> A diferencia de otros framework, donde se debe mapear cada método manualmente, Django detecta que esta vista es un "Conjunto de Acciones" (ViewSet) y deja que el **Router** (Punto 6) genere las URLs automáticamente.


### 6. Enrutamiento (URLs de Aplicación)
Se define el **punto de acceso (Endpoint)** donde React hará las peticiones.

**Crear el Archivo:** `apps/users/urls.py`

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserViewSet

# DefaultRouter: Generador automático de rutas. Crea las URLs para GET, POST, PUT y DELETE automáticamente.
# Él detecta que se usa en el ModelViewSet y crea las terminaciones de las rutas:
# /api/users/ (GET y POST)
# /api/users/ID/ (GET, PUT, PATCH, DELETE)
router = DefaultRouter()

# register: Asocia el prefijo de la URL con la lógica de la vista (UserViewSet).
# basename='user' asegura que Django sepa cómo llamar a las rutas internamente.
router.register(r'', UserViewSet, basename='user')
#La r antes de las comillas significa "Raw string" (Cadena en crudo). Es una buena práctica en Python para que los caracteres especiales (como las barras /) se lean tal cual, sin que Python intente interpretarlos como comandos.
#Al poner comillas vacías, se le dice al Router: "No agregue nada más a la dirección que ya esta dando el Core

urlpatterns = [
    # Rutas para el Login (Generación y refresco de Tokens)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # include: Incluye todas las rutas generadas por el router en la raíz de esta app.
    path('', include(router.urls)),
]
# include(router.urls): Registra esas rutas automáticas en el sistema para que cuando React las llame, Django sepa a dónde enviarlas.
```


### 7. Registro en el Núcleo (Core URLs)
Para que el sistema reconozca estas rutas, se debe asignar la dirección principal dentro del sistema global para que la aplicación sea visible.

**Archivo:** `core/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/'): Dirección para entrar al panel de control visual de Django.
    path('admin/', admin.site.urls),

    # path('api/users'): Prefijo global para la API. Conecta las URLs de la app 'users'.
    path('api/users/', include('apps.users.urls')),
]
```


## 8. 🏃 Lanzamiento del Servidor de Desarrollo
Comprobación final para asegurar que el backend está escuchando peticiones.

```bash
python manage.py runserver

# RESULTADO: El servidor debe informar que está corriendo en [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

#Para terminar la ejecucion usar Ctrl + C
```

---



## 9. 🛠️ Protocolo de Pruebas de la API (Paquetes JSON)
Usar esta guía para saber qué enviarle a la API desde herramientas como Postman o Insomnia antes de conectarlo con React.

### 📝 Guía de Intercambio de Datos (JSON)

| Acción | Método | URL | JSON de ejemplo (Body) | Respuesta Exitosa |
| :--- | :--- | :--- | :--- | :--- |
| **Registrar** | `POST` | `/api/users/` | `{"username":"j_alex", "password":"123", "email":"j@mail.com", "cedula":"1010"}` | `201 Created` |
| **Listar** | `GET` | `/api/users/` | (Enviar vacío) | `200 OK` (Lista de objetos) |
| **Ver Uno** | `GET` | `/api/users/1/` | (Enviar vacío) | `200 OK` (Objeto único) |
| **Editar** | `PATCH` | `/api/users/1/` | `{"cargo": "Administrador"}` | `200 OK` |
| **Borrar** | `DELETE` | `/api/users/1/` | (Enviar vacío) | `204 No Content` |

> **Nota:** En los métodos `GET` (individual), `PATCH`, `PUT` y `DELETE`, es obligatorio incluir el **ID** del usuario al final de la URL (ej: `/api/users/1/`).


## 10. 🔐 Pruebas con Autenticación (Flujo JWT en Postman)

Una vez que el modo de pruebas se desactiva (`MODO_PRUEBAS = False`), el sistema exigirá una llave digital (Token) para responder. Siga este flujo para validar los puntos de acceso protegidos.

### Paso 1: Obtención de la Llave (Login)
Para entrar al sistema, primero debemos solicitar las llaves de acceso enviando las credenciales de un usuario registrado.

1. **Método:** `POST`
2. **URL:** `http://127.0.0.1:8000/api/users/token/`
3. **Cuerpo (JSON):**
   ```json
   {
       "username": "tu_usuario",
       "password": "tu_contraseña"
   }
   ```
4. **Respuesta:** El servidor devolverá dos llaves: `access` (token temporal) y `refresh` (token para renovar el token temporal). Copie el valor de **access**.



### Paso 2: Configuración de la Petición Protegida
Para consultar datos protegidos (como listar usuarios), debemos presentar la llave en la cabecera de la petición.

1. Abra una nueva pestaña en Postman para una petición `GET` a `/api/users/`.
2. Diríjase a la pestaña **Authorization**.
3. En el campo **Type**, seleccione **Bearer Token**.
4. En el recuadro **Token**, pegue el código de la llave `access` que copió en el paso anterior.
5. Presione **Send**.

> **Nota Técnica:** > Postman automáticamente creará una cabecera oculta llamada `Authorization` con el valor `Bearer <tu_token>`. Este es el formato estándar que el filtro de seguridad de Django espera recibir.

---

## 11. 📝 Documentación de Endpoints (Contrato Backend-Frontend)

Para facilitar la integración con el equipo de Frontend (React), se recomienda mantener un registro detallado de cada punto de acceso. Esto actúa como un "contrato" que asegura que ambos equipos hablen el mismo idioma.

### Elementos clave del documento:
1. **URL y Método:** (Ej: `GET /api/users/`).
2. **Estructura del Request:** Lista de campos obligatorios y tipos de datos (String, Integer, Boolean).
3. **Códigos de Respuesta:**
   * `200 / 201`: Éxito.
   * `400`: Error de validación (Ej: "La cédula ya existe").
   * `401`: Token no enviado o vencido.
   * `403`: El usuario no tiene permisos suficientes.
4. **Esquema del JSON de respuesta:** Para que el Frontend sepa exactamente qué llaves (keys) vienen en el objeto y pueda mapearlas en la interfaz.

> [!TIP]
> **Automatización (Swagger):** > En etapas más avanzadas, podemos instalar herramientas como `drf-spectacular` que generan esta documentación de forma automática y visual, permitiendo que el equipo de Front pruebe los endpoints directamente desde el navegador.


---

## 12. ⚡ Población Automática de Datos (Seeders)
Para validar la arquitectura del sistema y los filtros de búsqueda sin realizar registros manuales, se utiliza un script de "siembra" de datos. Este proceso genera instancias de usuarios de prueba directamente en PostgreSQL.

**Crear el archivo:** `seed_users.py` (En la raíz del proyecto, junto a `manage.py`).

```python
import os
import django

# 1. Configuración del entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.users.models import User

def seed_data():
    # Lista de datos de prueba para la entidad Usuario
    usuarios_prueba = [
        {
            "username": "admin_central",
            "email": "admin@erp.com",
            "cedula": "900100",
            "cargo": "Gerente General",
            "empresa": "ERP Soluciones SAS"
        },
        {
            "username": "vendedor_01",
            "email": "ventas1@erp.com",
            "cedula": "800200",
            "cargo": "Asesor Comercial",
            "empresa": "Cliente Demo 1"
        }
    ]

    print("--- Iniciando persistencia de datos de prueba ---")

    for data in usuarios_prueba:
        # Verifica si el registro ya existe para evitar duplicados
        if not User.objects.filter(username=data["username"]).exists():
            User.objects.create_user(**data, password="Password123!")
            print(f"✅ Usuario creado: {data['username']}")
        else:
            print(f"⚠️ El usuario {data['username']} ya reside en la base de datos.")

    print("--- Proceso de población finalizado ---")

if __name__ == "__main__":
    seed_data()
```

### Ejecución del Script
Este comando dispara la lógica del script y vincula los datos con el motor de base de datos profesional.

```bash
# Ejecutar desde la terminal:
python seed_users.py
```

> [!TIP]
> **Seguridad en Producción:**
> Este archivo es exclusivamente para entornos de desarrollo y pruebas. Una vez que el sistema pase a producción, este script debe ser eliminado o protegido, ya que contiene la estructura base de los usuarios iniciales.

---
© 2026 - Proyecto ERP Colombiano - Desarrollo Profesional.


