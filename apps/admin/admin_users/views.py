from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated 
# Importa el nivel de acceso permitido, 
# AllowAny (Acceso a todo mundo) 
# IsAuthenticated (Acceso con token)
from django.conf import settings
from .models import AdminUser
from .serializers import AdminUserSerializer

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
        return [IsAuthenticated()]