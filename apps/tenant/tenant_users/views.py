from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from .models import TenantUser
from .serializers import TenantUserSerializer

class TenantUserViewSet(viewsets.ModelViewSet):
    """
    Conjunto de vistas (ViewSet) para la gestión integral de usuarios inquilinos.
    Provee automáticamente los endpoints para Listar, Crear, Recuperar, 
    Actualizar y Eliminar registros en la base de datos 'tenant'.
    """
    queryset = TenantUser.objects.all()
    serializer_class = TenantUserSerializer

    def get_permissions(self):
        """
        Implementa lógica de permisos dinámica basada en el entorno 
        y el tipo de acción ejecutada.
        """
        # Permite el registro público (creación) o acceso total en modo desarrollo
        if settings.DEBUG or self.action == 'create':
            return [AllowAny()]
        
        # Exige autenticación JWT para el resto de operaciones en producción
        return [IsAuthenticated()]