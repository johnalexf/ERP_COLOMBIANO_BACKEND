from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrganizationTypeViewSet, IdTypeViewSet, TaxRegimeViewSet, TaxResponsibilityViewSet

router = DefaultRouter()

router.register(r'organization-type', OrganizationTypeViewSet, basename= 'organization-type')
router.register(r'id-type', IdTypeViewSet, basename= 'id-type')
router.register(r'tax-regime', TaxRegimeViewSet, basename= 'tax-regime')
router.register(r'tax-responsibility', TaxResponsibilityViewSet, basename= 'tax-responsibility')

urlpatterns = [
    path( '' , include(router.urls)),
]