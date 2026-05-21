from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import  AdminUserViewSet, AdminLoginView, AdminTokenRefreshView

# DefaultRouter: Generador automático de rutas. Crea las URLs para GET, POST, PUT y DELETE automáticamente.
# Él detecta que se usa en el ModelViewSet y crea las terminaciones de las rutas:
# ruta/admin-user/ (GET y POST)
# ruta/admin-user/ID/ (GET, PUT, PATCH, DELETE)
router = DefaultRouter()

# register: Asocia el prefijo de la URL con la lógica de la vista (AdminUserViewSet).
# basename='admin-user' asegura que Django sepa cómo llamar a las rutas internamente.
# Registramos la vista bajo el subfijo 'admin-user'
router.register(r'admin-user', AdminUserViewSet, basename='admin-user')
#La r antes de las comillas significa "Raw string" (Cadena en crudo). Es una buena práctica en Python para que los caracteres especiales (como las barras /) se lean tal cual, sin que Python intente interpretarlos como comandos.
#Al poner comillas 'admin-user', se le dice al Router que agregue al final de la ruta /admin-user

urlpatterns = [
    # Rutas de Seguridad para el login (Generación y refresco de Tokens)
    path('auth/login/', AdminLoginView.as_view(), name='master_token_obtain_pair'),
    path('auth/refresh/', AdminTokenRefreshView.as_view(), name='master_token_refresh'),
    
    # include: Incluye todas las rutas generadas por el router en la raíz de esta app.
    # Rutas de Gestión (CRUD de Administradores generadas por el router)
    path('', include(router.urls)),
]
# include(router.urls): Registra esas rutas automáticas en el sistema para que cuando React las llame, Django sepa a dónde enviarlas.

