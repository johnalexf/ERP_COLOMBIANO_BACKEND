from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .models import AdminUser

class AdminJWTAuthentication(JWTAuthentication):
    """
    Motor de autenticación personalizado para la app Admin.
    Sobreescribe la búsqueda global de Django para hidratar a request.user
    estrictamente desde la tabla de AdminUser.
    """
    def get_user(self, validated_token):
        # Extraemos las reclamaciones (claims) del token
        user_id = validated_token.get('user_id')
        user_type = validated_token.get('user_type')

        # Doble validación: Bloqueo inmediato (Fail-Fast) si el token es de un Tenant
        if user_type != 'admin':
            raise AuthenticationFailed('Token inválido para el entorno administrativo.', code='invalid_token')

        # Buscamos explícitamente en nuestra base de datos administrativa
        try:
            user = AdminUser.objects.get(id=user_id)
        except AdminUser.DoesNotExist:
            raise AuthenticationFailed('Usuario administrador no encontrado.', code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed('Esta cuenta administrativa está inactiva.', code='user_inactive')

        # Retornamos el administrador validado
        return user