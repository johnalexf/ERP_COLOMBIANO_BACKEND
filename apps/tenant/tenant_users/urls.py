from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import TenantUserViewSet

# Inicialización del generador de rutas automáticas
router = DefaultRouter()

# Registro del prefijo 'tenant-user' vinculado a la lógica de inquilinos
router.register(r'tenant-user', TenantUserViewSet, basename='tenant-user')

urlpatterns = [
    # Endpoints de autenticación JWT para usuarios de negocio
    path('auth/login/', TokenObtainPairView.as_view(), name='tenant_token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='tenant_token_refresh'),
    
    # Inclusión de rutas CRUD generadas por el router
    path('', include(router.urls)),
]