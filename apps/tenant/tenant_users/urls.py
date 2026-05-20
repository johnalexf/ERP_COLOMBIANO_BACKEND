from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import TenantUserViewSet, TenantLoginView

# Inicialización del generador de rutas automáticas
router = DefaultRouter()

# Registro del prefijo 'tenant-user' vinculado a la lógica de inquilinos
router.register(r'tenant-user', TenantUserViewSet, basename='tenant-user')

urlpatterns = [
    # Endpoints de autenticación JWT para usuarios de negocio
    path('auth/login/', TenantLoginView.as_view(), name='tenant_token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='tenant_token_refresh'),
    
    # Inclusión de rutas CRUD generadas por el router
    path('', include(router.urls)),
]