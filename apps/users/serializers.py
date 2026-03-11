from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password # <--- Filtro de seguridad de Django
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Heredar de ModelSerializer otorga automáticamente las funciones de:
    LECTURA (List/Retrieve), EDICIÓN (Update/Patch) y ELIMINACIÓN (Delete).
    """

    # Definimos password como "solo escritura" (no se muestra en los GET)
    # Configuración de seguridad: React envía la clave (write), 
    # pero Django nunca la devuelve en el JSON de respuesta (read).
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        # Define el modelo de origen de los datos.
        model = User 
        
        # Lista blanca de campos que el serializador manejará.
        fields = ['id', 'username', 'password', 'email', 'cedula', 'telefono', 'cargo', 'empresa']

    # --- VALIDACIÓN DE CONTRASEÑA ---
    def validate_password(self, value):
        """
        Ejecuta los validadores de Django (longitud, claves comunes, etc.).
        Si la clave es débil (ej. '123'), lanzará un error 400 automáticamente.
        """
        validate_password(value)
        return value

    def create(self, validated_data):
        """
        Sobrescritura del método de creación para forzar la encriptación.
        .create_user: Método especial de Django que aplica Hashing a la contraseña.
        """
        user = User.objects.create_user(**validated_data)
        return user