from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Clase de permiso estricto para validar el origen del token JWT.
    Bloquea cualquier petición cuyo token no contenga la reclamación 'user_type'
    con el valor exacto 'admin', evitando cruces con accesos tenants.
    """

    def has_permission(self, request, view):
        # request.auth contiene el objeto del token desencriptado por SimpleJWT
        if request.auth:
            # Se extrae la etiqueta inyectada durante el login
            user_type = request.auth.get('user_type', None)
            
            # Retorna True (acceso permitido) solo si coincide exactamente
            return user_type == 'admin'
            
        # Bloqueo por defecto ante anomalías o ausencia de token
        return False