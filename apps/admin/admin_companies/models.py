from django.db import models
from apps.admin.admin_geography.models import Country, State, City
from apps.admin.admin_legal.models import OrganizationType, IdType, TaxRegime, TaxResponsibility

class LegalRepresentative(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name="País")

    first_name = models.CharField(max_length=100, verbose_name="Primer Nombre")
    middle_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Segundo Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Primer Apellido")
    second_last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Segundo Apellido")

    id_type = models.ForeignKey(IdType, on_delete=models.PROTECT, verbose_name="Tipo de identificación")
    identification_number = models.CharField(max_length=50, verbose_name="Número del documento")
    verification_digit = models.SmallIntegerField(null=True, blank=True, verbose_name="Dígito de verificación")
    phone_number = models.CharField(max_length=10, verbose_name="Número telefónico")
    email = models.EmailField(max_length=255, verbose_name="Correo electrónico")
    is_active = models.BooleanField(default=True, db_default=True, verbose_name="Estado Activo")

    class Meta:
        verbose_name = "Representante legal"
        verbose_name_plural = "Representantes legales"

    def __str__(self):
        # Une los nombres filtrando los valores que sean None o vacíos
        nombres = [self.first_name, self.middle_name, self.last_name, self.second_last_name]
        return " ".join(filter(None, nombres))


class Company(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name="País")
    state = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name="Departamento")
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Ciudad")

    address = models.CharField(max_length=255, verbose_name="Dirección")
    zip_code = models.CharField(max_length=15, null=True, blank=True, verbose_name="Código postal")

    organization_type = models.ForeignKey(OrganizationType, on_delete=models.PROTECT, verbose_name="Tipo de organización")
    legal_name = models.CharField(max_length=200, unique=True, verbose_name="Razón Social")
    trade_name = models.CharField(max_length=200, unique=True, verbose_name="Nombre Comercial")

    id_type = models.ForeignKey(IdType, on_delete=models.PROTECT, verbose_name="Tipo de identificación")
    tax_id = models.CharField(max_length=50, unique=True, verbose_name="Número de identificación")
    verification_digit = models.SmallIntegerField(null=True, blank=True, verbose_name="Dígito de verificación")

    tax_regime = models.ForeignKey(TaxRegime, on_delete=models.PROTECT, verbose_name="Régimen Fiscal")
    tax_responsibilities = models.ManyToManyField(TaxResponsibility, verbose_name="Responsabilidades Fiscales")

    phone_number = models.CharField(max_length=50, unique=True, verbose_name="Teléfono")
    email = models.EmailField(max_length=255, unique=True, verbose_name="Correo Electrónico")
    website = models.CharField(max_length=255, null=True, blank=True, unique=True, verbose_name="Página Web")
    
    legal_representative = models.OneToOneField(LegalRepresentative, on_delete=models.PROTECT, verbose_name="Representante legal")

    user_limit = models.PositiveIntegerField(verbose_name="Cantidad de usuarios permitidos")

    # Con auto_now=True Django gestiona las fechas automáticamente
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de modificación")

    # TODO:
    # El estado pago al dia se evaluara si desde el comienzo el pago se hara
    # desde la misma pagina para lo cual requiere su respectivo codigo
    # o si se hara de manera interna entre los encargados,
    # de igual manera queda pendiente determinar la programacion automatica de la fecha de expiracion
    expiration_date = models.DateField(verbose_name="Fecha de vencimiento")
    is_paid_up = models.BooleanField(default=True, db_default=True, verbose_name="Pago al dia")
    is_active = models.BooleanField(default=True, db_default=True, verbose_name="Estado activo")

    class Meta:
        verbose_name = "Compañía"
        verbose_name_plural = "Compañías"

    def __str__(self):
        return f"{self.legal_name} ({self.tax_id})"


class Branch(models.Model): 
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name="Compañía")

    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name="País")
    state = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name="Departamento")
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Ciudad")

    branch_name = models.CharField(max_length=150, unique=True, verbose_name="Nombre")

    address = models.CharField(max_length=255, verbose_name="Dirección")
    zip_code = models.CharField(max_length=15, null=True, blank=True, verbose_name="Código postal")

    phone_number = models.CharField(max_length=50, unique=True, verbose_name="Teléfono")
    email = models.EmailField(max_length=255, unique=True, verbose_name="Correo Electrónico")

    user_limit = models.PositiveIntegerField(verbose_name="Cantidad de usuarios permitidos")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de modificación")

    is_active = models.BooleanField(default=True, db_default=True, verbose_name="Estado activo")

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

    def __str__(self):
        return f"{self.company.legal_name} - {self.branch_name}"