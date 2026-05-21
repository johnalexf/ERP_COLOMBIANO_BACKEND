from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .models import TenantUser

class TenantJWTAuthentication(JWTAuthentication):
    """
    Motor de autenticación personalizado para la app Tenant.
    Sobreescribe la búsqueda global de Django para hidratar a request.user
    desde la tabla de TenantUser en lugar de la tabla global.
    """
    def get_user(self, validated_token):
        # Extraemos las reclamaciones (claims) del token
        user_id = validated_token.get('user_id')
        user_type = validated_token.get('user_type')

        # Doble validación: Aseguramos que el token sea del tipo correcto
        if user_type != 'tenant':
            raise AuthenticationFailed('Token inválido para este entorno.', code='invalid_token')

        # Buscamos explícitamente en nuestra base de datos de Tenant
        try:
            user = TenantUser.objects.get(id=user_id)
        except TenantUser.DoesNotExist:
            raise AuthenticationFailed('Usuario inquilino no encontrado.', code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed('Esta cuenta está inactiva.', code='user_inactive')

        # Retornamos el usuario. Esto llena la variable 'request.user' en la vista.
        return user