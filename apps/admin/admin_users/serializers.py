from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password # <--- Filtro de seguridad de Django
from .models import AdminUser

class AdminUserSerializer(serializers.ModelSerializer):
    """
    Traductor oficial para los usuarios del dominio administrativo.
    Heredar de ModelSerializer otorga automáticamente las funciones de:
    LECTURA (List/Retrieve), EDICIÓN (Update/Patch) y ELIMINACIÓN (Delete).
    """

    # Definimos password como "solo escritura" (write_only) no se muestra en los GET.
    # Configuración de seguridad: React envía la clave (write), 
    # pero Django nunca la devuelve en el JSON de respuesta (read) o al consultar datos.
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        # Define el modelo de origen de los datos.
        model = AdminUser
        
        # Lista blanca de campos permitidos en la API que el serializador manejará.
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'cargo_interno', 'telefono_contacto', 'is_active']

    # --- VALIDACIÓN DE CONTRASEÑA ---
    def validate_password(self, value):
        """
        Ejecuta los validadores nativos de Django (longitud, claves comunes, similitud).
        Si la clave es débil (ej. '123'), lanzará un error 400 automáticamente.
        """
        validate_password(value)
        return value

    def create(self, validated_data):
        """
        Sobrescritura VITAL del método de creación para forzar la encriptación.
        Se usa .create_user() para forzar el Hashing (encriptación) de la contraseña.
        """
        user = AdminUser.objects.create_user(**validated_data)
        return user


class AdminLoginSerializer(serializers.Serializer):
    """
    Serializador dedicado exclusivamente a la autenticación de Administradores.
    Permite iniciar sesión usando tanto el 'username' como el 'email'.
    """
    # Cambiamos EmailField por CharField y lo llamamos 'username' por convención estándar
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={"input_type": "password"}
    )

    def validate(self, data):
        # Capturamos el dato que el usuario escribió en el campo 'username'
        identificador = data.get("username")
        password = data.get("password")

        if identificador and password:
            try:
                # La Magia de Q: Busca coincidencias en email O en username
                user = AdminUser.objects.get(
                    Q(email=identificador) | Q(username=identificador)
                )
            except AdminUser.DoesNotExist:
                raise serializers.ValidationError("Credenciales inválidas o usuario no encontrado.")

            if not user.check_password(password):
                raise serializers.ValidationError("Credenciales inválidas.")

            if not user.is_active:
                raise serializers.ValidationError("Esta cuenta ha sido desactivada.")

            # Si todo está bien, adjuntamos el usuario validado
            data["user"] = user
            return data
            
        else:
            raise serializers.ValidationError("Debe proporcionar un usuario/email y contraseña.")