from django.db import models
from apps.admin.admin_geography.models import Country

class OrganizationType(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name="País")

    # TODO: legal_entity_code y abbreviation son nulos mientras se valida la lista correcta
    legal_entity_code = models.CharField(max_length=20, null=True, unique=True, verbose_name="Codigo camara de comercio")
    abbreviation = models.CharField(max_length=15, null=True, unique=True, verbose_name="Nomenclatura")
    name = models.CharField(max_length=150, unique=True, verbose_name="Nombre")
    is_active = models.BooleanField(default=True, db_default=True, verbose_name="Estado Activo")

    class Meta:
        verbose_name = "Tipo de organización"
        verbose_name_plural = "Tipos de organizaciones"
    
    def __str__(self):
        return f"{self.name} ({self.legal_entity_code})"


class IdType(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name="País")

    # TODO: id_type_code y abbreviation son nulos mientras se valida la lista correcta
    id_type_code = models.CharField(max_length=10, null=True, unique=True, verbose_name="Codigo legal")
    abbreviation = models.CharField(max_length=15, null=True, unique=True, verbose_name="Nomenclatura")
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    is_active = models.BooleanField(default=True, db_default=True, verbose_name="Estado Activo")

    class Meta:
        verbose_name = "Tipo de identificación"
        verbose_name_plural = "Tipos de identificaciones"
    
    def __str__(self):
        return f"{self.name} ({self.id_type_code})"
    

class TaxRegime(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name="País")

    # TODO: tax_regime_code es nulo mientras se valida la lista correcta
    tax_regime_code = models.CharField(max_length=20, null=True, unique=True, verbose_name="Codigo legal")
    abbreviation = models.CharField(max_length=15, null=True, unique=True, verbose_name="Nomenclatura")
    name = models.CharField(max_length=255, unique=True, verbose_name="Nombre")
    is_active = models.BooleanField(default=True, db_default=True, verbose_name="Estado Activo")

    class Meta:
        verbose_name = "Regimen fiscal"
        verbose_name_plural = "Regimenes fiscales"
    
    def __str__(self):
        return f"{self.name} ({self.tax_regime_code})"
    

class TaxResponsibility(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name="País")

    # TODO: tax_responsibility_code es nulo mientras se valida la lista correcta
    tax_responsibility_code = models.CharField(max_length=20, null=True, unique=True, verbose_name="Codigo legal")
    description = models.CharField(max_length=255, unique=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, db_default=True, verbose_name="Estado Activo")

    class Meta:
        verbose_name = "Responsabilidad fiscal"
        verbose_name_plural = "Responsabilidades fiscales"
    
    def __str__(self):
        return f"{self.name} ({self.tax_responsibility_code})"
