from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter 

from .models import Country, State, City
from .serializers import CountrySerializer, StateSerializer, CitySerializer

class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint de solo lectura para listar Países.
    Solo retorna países activos.
    """
    # El ORM busca en la base de datos
    queryset = Country.objects.filter(is_active=True)
    serializer_class = CountrySerializer


# Decorador para inyectar el parámetro en la documentación de Swagger de la acción 'list'
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='country',
                description='Filtrar departamentos por el ID del país.',
                required=False,
                type=int
            )
        ]
    )
)
class StateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint de solo lectura para listar Departamentos.
    Permite filtrado dinámico por país: /states/?country=1
    """
    serializer_class = StateSerializer

    def get_queryset(self):
        # Base: Traer todos los departamentos activos
        queryset = State.objects.filter(is_active=True)
        
        # Interceptar la URL buscando el parámetro '?country='
        country_id = self.request.query_params.get('country', None)
        
        # Si el frontend envió el filtro, aplicarlo en SQL
        if country_id is not None:
            queryset = queryset.filter(country_id=country_id)
            
        return queryset


# Decorador para la vista de ciudades
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='state',
                description='Filtrar ciudades por el ID del departamento.',
                required=False,
                type=int
            )
        ]
    )
)
class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint de solo lectura para listar Ciudades.
    Permite filtrado dinámico por departamento: /cities/?state=11
    """
    serializer_class = CitySerializer

    def get_queryset(self):
        # Base: Traer todas las ciudades activas
        queryset = City.objects.filter(is_active=True)
        
        # Interceptar la URL buscando el parámetro '?state='
        state_id = self.request.query_params.get('state', None)
        
        # Si el frontend envió el filtro, aplicarlo en SQL
        if state_id is not None:
            queryset = queryset.filter(state_id=state_id)
            
        return queryset
