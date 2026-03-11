from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Extensión de la interfaz para el Usuario Personalizado
class CustomUserAdmin(UserAdmin):
    # Columnas visibles en el listado general
    list_display = ('username', 'email', 'cedula', 'empresa', 'is_staff')
    
    # Organización de los campos en el formulario de edición (Detalle)
    # Se mantienen los campos estándar y se anexa la "Información de Negocio"
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Negocio', {
            'fields': ('cedula', 'telefono', 'cargo', 'empresa')
        }),
    )

# Registro del modelo bajo la nueva configuración
admin.site.register(User, CustomUserAdmin)