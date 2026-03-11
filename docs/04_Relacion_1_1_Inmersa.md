# 🏗️ Relación Uno a Uno (1:1) - Configuración Inmersa

Este documento describe cómo implementar una relación 1:1 dentro de una misma aplicación. Se utiliza cuando una entidad requiere datos adicionales que, por orden y limpieza, no deben estar en la tabla principal pero pertenecen al mismo módulo.

Funciona como un **"anexo de contrato"**: un registro solo puede tener un único complemento. En la base de datos, esto crea una **Llave Foránea con restricción UNIQUE**.


---
## 1. Definición del Modelo (Estructura Inmersa)
Ambas clases residen en el mismo archivo para mantener la cohesión del módulo.

**Archivo:** `apps/users/models.py`

```python
from django.db import models
from django.conf import settings

# Clase 01: La entidad principal ya existe (User)

# Clase 02: El complemento (Perfil)
class Perfil(models.Model):
    # OneToOneField: Asegura que un usuario solo tenga UN perfil y viceversa.
    # on_delete=models.CASCADE: Si se borra el usuario, se borra el perfil.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    
    biografia = models.TextField(blank=True, null=True)
    preferencias_color = models.CharField(max_length=20, default='blue')
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)

    def __str__(self):
        return f"Perfil de: {self.user.username}"
```

---

## 2. Serialización Anidada (Traducción para React)
Para que el Frontend reciba los datos del Usuario y del Perfil en una sola petición, debemos "anidar" los serializadores.

**Archivo:** `apps/users/serializers.py`

```python
from rest_framework import serializers
from .models import User, Perfil

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['biografia', 'preferencias_color', 'foto_perfil']

class UserSerializer(serializers.ModelSerializer):
    # Anidamos el perfil para que aparezca como un objeto dentro del usuario
    perfil = PerfilSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'cedula', 'cargo', 'perfil']
```



---

## 3. Lógica de Activación Automática (Signals)
En las relaciones 1:1 inmersas, es una buena práctica que el perfil se cree automáticamente cuando se registra un usuario nuevo.

**Archivo:** `apps/users/models.py` (Al final del archivo)

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    # Si el usuario es nuevo, le creamos su "cajón" de perfil vacío
    if created:
        Perfil.objects.create(user=instance)
```

---

## 4. Persistencia (Migraciones)
Al ser cambios en los modelos, se debe actualizar la base de datos profesional.

```bash
# 1. Generar el script de cambio
python manage.py makemigrations users

# 2. Aplicar a PostgreSQL
python manage.py migrate
```

---

## 5. Validación en el Endpoint

Al usar el `ModelViewSet` en las vistas, los puntos de acceso se activan automáticamente.

Al consultar `/api/users/`, la respuesta exitosa debe verse así:

```json
{
    "id": 1,
    "username": "j_alex",
    "email": "alex@erp.com",
    "perfil": {
        "biografia": "Desarrollador Senior",
        "preferencias_color": "blue",
        "foto_perfil": null
    }
}
```

---
© 2026 - Proyecto ERP Colombiano - Desarrollo Profesional.

