from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import TenantUser


class TenantUserSerializer(serializers.ModelSerializer):
    """
    Serializador de grado industrial para la gestión de usuarios de inquilinos.
    Implementa validaciones estrictas de seguridad y encriptación de credenciales.
    """

    # Configuración de seguridad para el campo de contraseña
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = TenantUser
        # Definición de campos expuestos en la interfaz de la API
        fields = [
            "id",
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "second_last_name",
            "password",
            "is_active",
            "date_joined",
        ]

    def validate_password(self, value):
        """
        Invoca los validadores de seguridad configurados en el núcleo del sistema
        para asegurar la robustez de la contraseña del cliente.
        """
        validate_password(value)
        return value

    def create(self, validated_data):
        """
        Al heredar de AbstractBaseUser, no existe el método 'create_user'.
        Por lo tanto, creamos la instancia, encriptamos la clave manualmente 
        con set_password() y luego guardamos en la base de datos.
        """
        # 1. Sacamos la contraseña del diccionario de datos
        password = validated_data.pop('password')
        
        # 2. Creamos el usuario con los datos restantes (sin guardar aún en la BD)
        user = TenantUser(**validated_data)
        
        # 3. Encriptamos la contraseña
        user.set_password(password)
        
        # 4. Guardamos físicamente en PostgreSQL
        user.save()
        
        return user
