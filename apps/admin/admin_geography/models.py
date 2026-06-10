from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    iso_code_3 = models.CharField(max_length=3, unique=True, verbose_name="Nomenclatura ISO3")
    phone_code = models.CharField(max_length=5, verbose_name="Prefijo Telefónico")
    is_active = models.BooleanField(default=True, db_default=True, verbose_name="Estado Activo")

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"

    def __str__(self):
        return f"{self.name} ({self.iso_code_3})"


class State(models.Model):
    # Relación con País. PROTECT evita borrar un país con departamentos.
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name="País")
    
    state_code = models.CharField(max_length=10, unique=True, verbose_name="Código de Departamento")
    name = models.CharField(max_length=100, verbose_name="Nombre")
    is_active = models.BooleanField(default=True, db_default=True, verbose_name="Estado Activo")

    class Meta:
        verbose_name = "Departamento / Estado"
        verbose_name_plural = "Departamentos / Estados"

    def __str__(self):
        return f"{self.name} - {self.country.iso_code_3}"


class City(models.Model):
    # Relación con Departamento
    state = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name="Departamento")
    
    city_code = models.CharField(max_length=15, unique=True, verbose_name="Código de Ciudad")
    name = models.CharField(max_length=100, verbose_name="Nombre")
    is_active = models.BooleanField(default=True, db_default=True, verbose_name="Estado Activo")

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"

    def __str__(self):
        return f"{self.name} ({self.state.name})"