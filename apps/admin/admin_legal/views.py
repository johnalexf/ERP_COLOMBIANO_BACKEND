from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from .models import OrganizationType, IdType, TaxRegime, TaxResponsibility
from .serializers import OrganizationTypeSerializers, IdTypeSerializers, TaxRegimeSerializers, TaxResponsibilitySerializers


# ---------------------- Configuracion de la vista para el modelo OrganizationType ----------------------

# Agregando instrucciones en la documentacion automatica del filtrado por país
@extend_schema_view(
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                name = 'country',
                description = 'Filtrar tipos de organizaciones por país.',
                required = False,
                type = int
            )
        ]
    )
)
class OrganizationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint de solo lectura para listar tipo de organizaciones
    Solo retorna las que esten activas
    y Permite filtrado dinámico por país: /organization-type/?country=1
    """

    serializer_class = OrganizationTypeSerializers

    def get_queryset(self):

        queryset = OrganizationType.objects.filter(is_active = True)

        country_id = self.request.query_params.get('country', None)

        if country_id is not None:
            queryset = queryset.filter(country_id = country_id)

        return queryset



# ---------------------- Configuracion de la vista para el modelo IdType ----------------------

# Agregando instrucciones en la documentacion automatica del filtrado por país
@extend_schema_view(
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                name = 'country',
                description = 'Filtrar tipo de identificación por país.',
                required = False,
                type = int
            )
        ]
    )
)
class IdTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint de solo lectura para listar tipo de identificación
    Solo retorna las que esten activas
    y Permite filtrado dinámico por país: /id-type/?country=1
    """

    serializer_class = IdTypeSerializers

    def get_queryset(self):

        queryset = IdType.objects.filter(is_active = True)

        country_id = self.request.query_params.get('country', None)

        if country_id is not None:
            queryset = queryset.filter(country_id = country_id)

        return queryset



# ---------------------- Configuracion de la vista para el modelo TaxRegime ----------------------

# Agregando instrucciones en la documentacion automatica del filtrado por país
@extend_schema_view(
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                name = 'country',
                description = 'Filtrar regimen fiscal por país.',
                required = False,
                type = int
            )
        ]
    )
)
class TaxRegimeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint de solo lectura para listar regimenes fiscales
    Solo retorna las que esten activas
    y Permite filtrado dinámico por país: /tax-regime/?country=1
    """

    serializer_class = TaxRegimeSerializers

    def get_queryset(self):

        queryset = TaxRegime.objects.filter(is_active = True)

        country_id = self.request.query_params.get('country', None)

        if country_id is not None:
            queryset = queryset.filter(country_id = country_id)

        return queryset
    


# ---------------------- Configuracion de la vista para el modelo TaxResponsibility ----------------------

# Agregando instrucciones en la documentacion automatica del filtrado por país
@extend_schema_view(
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                name = 'country',
                description = 'Filtrar responsabilidades fiscales por país.',
                required = False,
                type = int
            )
        ]
    )
)
class TaxResponsibilityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint de solo lectura para listar responsabilidades fiscales
    Solo retorna las que esten activas
    y Permite filtrado dinámico por país: /tax-responsibility/?country=1
    """

    serializer_class = TaxResponsibilitySerializers

    def get_queryset(self):

        queryset = TaxResponsibility.objects.filter(is_active = True)

        country_id = self.request.query_params.get('country', None)

        if country_id is not None:
            queryset = queryset.filter(country_id = country_id)

        return queryset