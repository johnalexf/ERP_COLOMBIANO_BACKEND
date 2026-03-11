from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    # El 'name' es la ruta física (donde está la carpeta)
    name = 'apps.users'
    
    # El 'label' es el nombre corto interno (direccion logica para evitar problemas con la búsqueda desde el núcleo hasta la app)
    label = 'users'