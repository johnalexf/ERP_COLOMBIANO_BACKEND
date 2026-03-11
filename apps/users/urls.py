from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserViewSet

# DefaultRouter: Generador automático de rutas. Crea las URLs para GET, POST, PUT y DELETE automáticamente.
# Él detecta que se usa en el ModelViewSet y crea las terminaciones de las rutas:
# /api/users/ (GET y POST)
# /api/users/ID/ (GET, PUT, PATCH, DELETE)
router = DefaultRouter()

# register: Asocia el prefijo de la URL con la lógica de la vista (UserViewSet).
# basename='user' asegura que Django sepa cómo llamar a las rutas internamente.
router.register(r'', UserViewSet, basename='user')
#La r antes de las comillas significa "Raw string" (Cadena en crudo). Es una buena práctica en Python para que los caracteres especiales (como las barras /) se lean tal cual, sin que Python intente interpretarlos como comandos.
#Al poner comillas vacías, se le dice al Router: "No agregue nada más a la dirección que ya esta dando el Core

urlpatterns = [
    # Rutas para el Login (Generación y refresco de Tokens)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # include: Incluye todas las rutas generadas por el router en la raíz de esta app.
    path('', include(router.urls)),
]
# include(router.urls): Registra esas rutas automáticas en el sistema para que cuando React las llame, Django sepa a dónde enviarlas.