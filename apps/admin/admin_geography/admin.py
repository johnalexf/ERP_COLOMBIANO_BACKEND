from django.contrib import admin
from .models import Country, State, City

# TODO:
# El portal administrativo permanecerá habilitado durante las primeras etapas del proyecto.
# Antes de pasar a producción se debe definir qué operaciones estarán permitidas
# sobre los catálogos maestros (crear, editar, eliminar o solo consultar).
#
# Esta decisión se tomará antes del registro del primer cliente o durante la
# fase de endurecimiento de seguridad del sistema.

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'iso_code_3', 'phone_code', 'is_active')
    search_fields = ('name', 'iso_code_3', 'phone_code')
    list_filter = ('is_active',)
    ordering = ('name',)

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state_code', 'country', 'is_active')
    search_fields = ('name', 'state_code')
    list_filter = ('country', 'is_active')
    ordering = ('country', 'name')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city_code', 'state', 'is_active')
    search_fields = ('name', 'city_code')
    # Filtro avanzado: permite filtrar por departamento y por país del departamento
    list_filter = ('state__country', 'state', 'is_active')
    ordering = ('state', 'name')