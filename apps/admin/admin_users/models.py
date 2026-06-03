from django.contrib.auth.models import AbstractUser
from django.db import models

class AdminUser(AbstractUser):
    """
    Modelo de usuario maestro para los administradores y dueños del ERP.
    Por directriz del ErpDatabaseRouter, esta tabla existirá 
    exclusivamente en la base de datos 'default'.
    Hereda: username, password, email, first_name, last_name, date_joined, is_staff, is_active.
    """
    # Sobrescribimos el email para forzar a que sea único y obligatorio
    email = models.EmailField(unique=True, max_length=255, verbose_name='Correo Electrónico')
    
    phone_number = models.CharField(max_length=10, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = 'Usuario Administrador'
        verbose_name_plural = 'Usuarios Administradores'

    def __str__(self):
        return f"{self.username} ({self.email})"