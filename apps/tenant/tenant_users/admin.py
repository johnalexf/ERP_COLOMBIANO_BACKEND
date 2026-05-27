from django.contrib import admin
from .models import TenantUser, TenantRol, TenantPermission

class TenantModelAdmin(admin.ModelAdmin):
    """
    Controlador maestro para forzar el enrutamiento de operaciones
    del panel administrativo hacia la base de datos 'tenant'.
    """
    using = 'tenant'

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


class TenantUserAdmin(TenantModelAdmin):
    # Configuración de visualización para el modelo AbstractBaseUser
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'date_joined')
    ordering = ('-date_joined',)

# Registro de entidades bajo la regla de enrutamiento estricto
admin.site.register(TenantUser, TenantUserAdmin)
admin.site.register(TenantRol, TenantModelAdmin)
admin.site.register(TenantPermission, TenantModelAdmin)