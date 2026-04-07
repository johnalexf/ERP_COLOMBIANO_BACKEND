from django.apps import AppConfig

class AdminUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    # La ruta física exacta
    name = 'apps.admin.admin_users'
    
    # El nombre interno que lee nuestro ErpDatabaseRouter
    label = 'admin_users'