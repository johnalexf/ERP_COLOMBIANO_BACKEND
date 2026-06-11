from rest_framework import serializers
from .models import OrganizationType, IdType, TaxRegime, TaxResponsibility

class OrganizationTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model=OrganizationType
        fields = ['id', 'legal_entity_code', 'abbreviation', 'name']

class IdTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = IdType
        fields = ['id', 'id_type_code', 'abbreviation', 'name']

class TaxRegimeSerializers(serializers.ModelSerializer):
    class Meta:
        model = TaxRegime
        fields = ['id', 'tax_regime_code', 'abbreviation', 'name']

class TaxResponsibilitySerializers(serializers.ModelSerializer):
    class Meta:
        model = TaxResponsibility
        fields = ['id', 'tax_responsibility_code', 'description']
