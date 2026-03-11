from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Escáner de Identidad: Permite la autenticación híbrida 
    usando el Nombre de Usuario o el Correo Electrónico.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Filtro de búsqueda: Buscamos coincidencia exacta en 'username' O 'email'
            # iexact se usa para que no importe si escriben en Mayúsculas o Minúsculas
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            # Si no hay coincidencia en ninguna columna, el acceso se deniega
            return None
        except UserModel.MultipleObjectsReturned:
            # En caso de colisión (duplicados), devuelve el primero que encuentre
            return UserModel.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username)
            ).first()

        # Verificación del "Password": Si el usuario existe, validamos su contraseña
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None