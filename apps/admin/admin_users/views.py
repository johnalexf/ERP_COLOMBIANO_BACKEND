from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
# Importa el nivel de acceso permitido, 
# AllowAny (Acceso a todo mundo) 
# IsAuthenticated (Acceso con token)
from django.conf import settings
from .models import AdminUser
from .serializers import AdminUserSerializer, AdminLoginSerializer

from .permissions import IsAdminUser

# True para desarrollo, False para producción
MODO_PRUEBAS = settings.DEBUG

class AdminUserViewSet(viewsets.ModelViewSet):
# viewsets.ModelViewSet: Clase maestra que ya incluye la lógica para Listar, Crear, Ver, Editar y Borrar.
    """
    - Listar (GET /)
    - Crear (POST /)
    - Ver detalle (GET /id/)
    - Editar (PUT-PATCH /id/)
    - Borrar (DELETE /id/)
    """
    queryset = AdminUser.objects.all() 
    # queryset: Define la consulta a la base de datos (En este caso, traer todos los usuarios).

    serializer_class = AdminUserSerializer 
    # serializer_class: Especifica qué "traductor" JSON usará esta vista.

    # get_permissions(self) Define el protocolo de seguridad. AllowAny abre la puerta para pruebas iniciales.
    def get_permissions(self):
        # Si estamos en modo desarrollador O si se está intentando crear un usuario, puerta abierta.
        if MODO_PRUEBAS or self.action == 'create':
            return [AllowAny()]
        
        # Para el resto de acciones en producción, se exige un Token JWT válido.
        return [IsAuthenticated(),IsAdminUser()]
    

class AdminLoginView(APIView):
    """
    Clase basada en APIView encargada de procesar la autenticación 
    de usuarios de tipo Admin y emitir los tokens JWT correspondientes.
    """
    # Asignamos el serializador exclusivo para el login de administradores
    serializer_class = AdminLoginSerializer

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
        refresh['user_type'] = 'admin'
        
        # Retorno de respuesta HTTP 200 con el payload de tokens
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Autenticación exitosa.'
        }, status=status.HTTP_200_OK)