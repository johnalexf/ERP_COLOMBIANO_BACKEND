from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

# ---------------------------------------------------------
# TABLAS DE SEGURIDAD BASE
# ---------------------------------------------------------

class TenantPermission(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre del permiso')
    codename = models.CharField(max_length=100, unique=True, verbose_name='Código Interno')

    class Meta:
        verbose_name = 'Permiso de Inquilino'
        verbose_name_plural = 'Permisos de Inquilinos'

    def __str__(self):
        return self.name

class TenantRol(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre del Rol')
    permission = models.ManyToManyField(TenantPermission, blank=True, verbose_name='Permisos Asignados')

    class Meta:
        verbose_name = 'Rol de Inquilino'
        verbose_name_plural = 'Roles de Inquilinos'

    def __str__(self):
        return self.name

# ---------------------------------------------------------
# TABLA PRINCIPAL: USUARIO INQUILINO (Plantilla)
# ---------------------------------------------------------

class TenantUser(AbstractBaseUser):
    """
    Plantilla base de autenticación.
    Estrictamente variables en inglés. Cero lógica de negocio aún.
    """
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    
    first_name = models.CharField(max_length=50, verbose_name='Primer Nombre')
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Segundo Nombre')
    last_name = models.CharField(max_length=50, verbose_name='Primer Apellido')
    second_last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Segundo Apellido')
    
    is_active = models.BooleanField(default=True, verbose_name='Estado Activo')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Fecha de registro')

    USERNAME_FIELD = 'email'
    
    class Meta:
        verbose_name = 'Usuario Inquilino'
        verbose_name_plural = 'Usuarios Inquilinos'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"