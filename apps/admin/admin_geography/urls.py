from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CountryViewSet, StateViewSet, CityViewSet

# Instanciamos el enrutador automático
router = DefaultRouter()

# Registramos las tres rutas.
# Esto generará automáticamente:
# GET /countries/
# GET /states/ (y acepta ?country=X)
# GET /cities/ (y acepta ?state=X)
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'states', StateViewSet, basename='state')
router.register(r'cities', CityViewSet, basename='city')

urlpatterns = [
    # Incluimos todas las rutas generadas por el router en la raíz de esta app
    path('', include(router.urls)),
]