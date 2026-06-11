from django.contrib import admin
from .models import OrganizationType, IdType, TaxRegime, TaxResponsibility

# TODO:
# El portal administrativo permanecerá habilitado durante las primeras etapas del proyecto.
# Antes de pasar a producción se debe definir qué operaciones estarán permitidas
# sobre los catálogos maestros (crear, editar, eliminar o solo consultar).
#
# Esta decisión se tomará antes del registro del primer cliente o durante la
# fase de endurecimiento de seguridad del sistema.

@admin.register(OrganizationType)
class OrganizationTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'legal_entity_code', 'abbreviation', 'country', 'is_active')
    search_fields = ('name', 'legal_entity_code', 'abbreviation')
    list_filter = ('country', 'is_active')

@admin.register(IdType)
class IdTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'id_type_code', 'abbreviation', 'country', 'is_active')
    search_fields = ('name', 'id_type_code', 'abbreviation')
    list_filter = ('country', 'is_active')

@admin.register(TaxRegime)
class TaxRegimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tax_regime_code', 'abbreviation', 'country', 'is_active')
    search_fields = ('name', 'tax_regime_code', 'abbreviation')
    list_filter = ('country', 'is_active')

@admin.register(TaxResponsibility)
class TaxResponsibilityAdmin(admin.ModelAdmin):
    # Usamos 'description' en lugar de 'name' tal como lo definiste
    list_display = ('id', 'description', 'tax_responsibility_code', 'country', 'is_active')
    search_fields = ('description', 'tax_responsibility_code')
    list_filter = ('country', 'is_active')