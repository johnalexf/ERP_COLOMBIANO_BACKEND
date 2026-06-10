from rest_framework import serializers
from .models import Country, State, City

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        # Exponemos todos los campos útiles para el frontend
        fields = ['id', 'name', 'iso_code_3', 'phone_code']

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        # Incluimos 'country' que devolverá automáticamente el ID del país al que pertenece
        fields = ['id', 'country', 'state_code', 'name']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        # Incluimos 'state' que devolverá automáticamente el ID del departamento
        fields = ['id', 'state', 'city_code', 'name']