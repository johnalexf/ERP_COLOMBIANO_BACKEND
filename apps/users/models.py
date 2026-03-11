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