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


class TenantLoginSerializer(serializers.Serializer):
    """
    Serializador dedicado exclusivamente a la autenticación de Tenants.
    Ignora el backend global de Django para evitar cruces con AdminUser.
    """
    # 1. Exigimos explícitamente email en lugar de username
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={"input_type": "password"}
    )

    def validate(self, data):
        """
        Sobreescribimos la validación general. Aquí interceptamos el JSON
        y aplicamos nuestra propia lógica de negocio para iniciar sesión.
        """
        email = data.get("email")
        password = data.get("password")

        if email and password:
            # 2. Reemplazamos la función global authenticate()
            # Buscamos ESTRICTAMENTE en la tabla de TenantUser
            try:
                user = TenantUser.objects.get(email=email)
            except TenantUser.DoesNotExist:
                # Si es un Admin intentando entrar, fallará aquí mismo
                raise serializers.ValidationError("Credenciales inválidas o usuario no encontrado.")

            # 3. Comprobamos el hasheo de la contraseña
            if not user.check_password(password):
                raise serializers.ValidationError("Credenciales inválidas.")

            # 4. Validamos que la cuenta no esté bloqueada
            if not user.is_active:
                raise serializers.ValidationError("Esta cuenta ha sido desactivada.")

            # Si pasa todas las pruebas, inyectamos el usuario en los datos
            # para que la Vista lo pueda tomar y generar el token.
            data["user"] = user
            return data
            
        else:
            raise serializers.ValidationError("Debe proporcionar email y contraseña.")
