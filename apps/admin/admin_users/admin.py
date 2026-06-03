from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AdminUser

class CustomAdminUserAdmin(UserAdmin):
    # Columnas expuestas en la vista de lista
    list_display = ('username', 'email', 'phone_number', 'is_staff')
    
    # Inyección de campos personalizados en la vista de detalle
    fieldsets = UserAdmin.fieldsets + (
        ('Información Interna ERP', {
            'fields': ('phone_number',)
        }),
    )

# Registro del modelo en el ecosistema Admin
admin.site.register(AdminUser, CustomAdminUserAdmin)