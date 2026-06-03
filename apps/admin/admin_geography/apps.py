from django.apps import AppConfig


class AdminGeographyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.admin.admin_geography' # Ruta física exacta
    label = 'admin_geography' # Nombre interno para el router