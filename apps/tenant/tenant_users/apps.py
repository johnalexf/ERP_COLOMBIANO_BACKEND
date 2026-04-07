from django.apps import AppConfig

class TenantUsersConfig(AppConfig):
    # Todos los id internos seran de tipo BigAutoField
    default_auto_field = 'django.db.models.BigAutoField'
    
    # La ruta física exacta
    name = 'apps.tenant.tenant_users'
    
    # El nombre interno que lee nuestro ErpDatabaseRouter
    label = 'tenant_users'