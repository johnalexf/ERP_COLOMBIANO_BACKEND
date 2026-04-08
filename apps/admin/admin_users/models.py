from django.contrib.auth.models import AbstractUser
from django.db import models

class AdminUser(AbstractUser):
    """
    Modelo de usuario maestro para los administradores y dueños del ERP.
    Por directriz del ErpDatabaseRouter, esta tabla existirá 
    exclusivamente en la base de datos 'default'.
    """
    # Sobrescribimos el email para forzar a que sea único y obligatorio
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    
    # Campos personalizados exclusivos para la administración interna
    cargo_interno = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text="Ej: Soporte Nivel 1, Arquitecto de Software, Gerente"
    )
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Usuario Administrador'
        verbose_name_plural = 'Usuarios Administradores'

    def __str__(self):
        return f"{self.username} ({self.cargo_interno or 'Sin cargo asignado'})"