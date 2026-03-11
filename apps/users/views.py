from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated 
# Importa el nivel de acceso permitido, 
# AllowAny (Acceso a todo mundo) 
# IsAuthenticated (Acceso con token)
from .models import User
from .serializers import UserSerializer

# True para desarrollo, False para producción
MODO_PRUEBAS = settings.DEBUG

class UserViewSet(viewsets.ModelViewSet):
# viewsets.ModelViewSet: Clase maestra que ya incluye la lógica para Listar, Crear, Ver, Editar y Borrar.
    """
    ModelViewSet concentra en una sola clase las 5 acciones del CRUD:
    - Listar (GET /)
    - Crear (POST /)
    - Ver detalle (GET /id/)
    - Editar (PUT-PATCH /id/)
    - Borrar (DELETE /id/)
    """
    queryset = User.objects.all() 
    # queryset: Define la consulta a la base de datos (En este caso, traer todos los usuarios).

    serializer_class = UserSerializer 
    # serializer_class: Especifica qué "traductor" JSON usará esta vista.

    permission_classes = [AllowAny] if MODO_PRUEBAS else [IsAuthenticated]
    # permission_classes: Define el protocolo de seguridad. AllowAny abre la puerta para pruebas iniciales.