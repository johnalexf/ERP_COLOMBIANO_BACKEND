from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .models import TenantUser
from .serializers import TenantUserSerializer, TenantLoginSerializer, TenantTokenRefreshSerializer

from .permissions import IsTenantUser
from .authentication import TenantJWTAuthentication

class TenantUserViewSet(viewsets.ModelViewSet):
    """
    Conjunto de vistas (ViewSet) para la gestión integral de usuarios inquilinos.
    Provee automáticamente los endpoints para Listar, Crear, Recuperar, 
    Actualizar y Eliminar registros en la base de datos 'tenant'.
    """
    queryset = TenantUser.objects.all()
    serializer_class = TenantUserSerializer

    # 1. AUTENTICACIÓN: "¿Es un usuario en la base de datos Tenant?" 
    authentication_classes = [TenantJWTAuthentication]

    def get_permissions(self):
        """
        Implementa lógica de permisos dinámica basada en el entorno 
        y el tipo de acción ejecutada.
        """
        # Permite el registro público (creación).
        if self.action == 'create':
            return [AllowAny()]
        
        # Exige autenticación JWT para el resto de operaciones en producción
        # Se exige autenticación válida Y que el token pertenezca a un Tenant
        return [IsAuthenticated(), IsTenantUser()]


class TenantLoginView(APIView):
    """
    Clase basada en APIView encargada de procesar la autenticación 
    de usuarios de tipo Tenant y emitir los tokens JWT correspondientes.
    """
    
    # Asignación del serializador para la validación de credenciales
    serializer_class = TenantLoginSerializer

    def post(self, request):
        """
        Procesa las peticiones POST entrantes con las credenciales del usuario.
        """
        # Instanciación del serializador con el payload HTTP entrante
        serializer = self.serializer_class(data=request.data)
        
        # Ejecución del proceso de validación. Lanza excepción HTTP 400 si la validación falla.
        serializer.is_valid(raise_exception=True)
        
        # Extracción de la instancia del modelo validado
        user = serializer.validated_data['user']
        
        # Generación de tokens de acceso base y refresco vía SimpleJWT
        refresh = RefreshToken.for_user(user)

        # INYECCIÓN DEL CLAIM: Se añade el tipo de usuario al payload del JWT
        refresh['user_type'] = 'tenant'
        
        # Retorno de respuesta HTTP 200 con el payload de tokens
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Autenticación exitosa.'
        }, status=status.HTTP_200_OK)
    

class TenantTokenRefreshView(TokenRefreshView):
    """
    Vista personalizada para emisión de nuevos Access Tokens para inquilinos.
    """
    serializer_class = TenantTokenRefreshSerializer