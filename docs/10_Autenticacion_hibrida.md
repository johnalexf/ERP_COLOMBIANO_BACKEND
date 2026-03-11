# Manual 10: Autenticación Híbrida (Escáner de Identidad)

Este componente actúa como un **filtro inteligente** que permite al sistema de seguridad (Django y SimpleJWT) validar credenciales comparando el dato ingresado contra dos columnas de la base de datos de manera simultánea: `username` y `email`.

### 1. 🏗️ Implementación del Backend de Autenticación

En tu estructura de carpetas, navega hasta tu aplicación de usuarios (ej: `apps/users/`) y crea un archivo nuevo llamado **`backends.py`**.

```python
# apps/users/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Escáner de Identidad: Permite la autenticación híbrida 
    usando el Nombre de Usuario o el Correo Electrónico.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Filtro de búsqueda: Buscamos coincidencia exacta en 'username' O 'email'
            # iexact se usa para que no importe si escriben en Mayúsculas o Minúsculas
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            # Si no hay coincidencia en ninguna columna, el acceso se deniega
            return None
        except UserModel.MultipleObjectsReturned:
            # En caso de colisión (duplicados), devuelve el primero que encuentre
            return UserModel.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username)
            ).first()

        # Verificación del "Password": Si el usuario existe, validamos su contraseña
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
```

### 2. ⚙️ Vinculación en la Configuración Maestra

Para que Django "active" este nuevo escáner, debemos registrarlo en el archivo de configuración global. 

**Archivo:** `core/settings.py`

```python
# --- CONFIGURACIÓN DE SISTEMAS DE AUTENTICACIÓN ---

AUTHENTICATION_BACKENDS = [
    # 1. Tu nuevo Escáner Híbrido (ajusta la ruta según el nombre de tu app)
    'apps.users.backends.EmailOrUsernameModelBackend',
    
    # 2. El sistema estándar de Django (mantenido como respaldo)
    'django.contrib.auth.backends.ModelBackend',
]
```

> [!IMPORTANT]
> **Nota de Arquitecto:** Al colocar tu nuevo backend en la primera posición de la lista, le das **prioridad**. Django intentará validar por usuario/correo primero y, si falla, usará el método tradicional.

### 3. 🧪 Protocolo de Validación

Una vez guardados los cambios, el sistema responderá de la siguiente manera ante una petición de Token (`/api/token/`):

| Entrada del Usuario | Lógica del Backend | Resultado Esperado |
| :--- | :--- | :--- |
| **"john_forero"** | Busca en columna `username`. | **Token Generado** ✅ |
| **"john@erp.com"** | Busca en columna `email`. | **Token Generado** ✅ |
| **"dato_erroneo"** | No encuentra coincidencia. | **401 Unauthorized** ❌ |

---

### 🧠 Justificación Técnica (SimpleJWT vs Allauth)

Aunque `django-allauth` tiene reglas para permitir el login híbrido, el motor de **SimpleJWT** es un componente independiente que solo consulta el `ModelBackend` por defecto (el cual solo mira el campo `username`). 

Este archivo `backends.py` es el **puente técnico** necesario para que la versatilidad de `allauth` sea heredada por los endpoints de la API (React).

---
© 2026 - Proyecto ERP Colombiano - Arquitectura de Seguridad.