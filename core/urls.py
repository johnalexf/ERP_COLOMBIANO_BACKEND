"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)

# Rutas que SIEMPRE van a existir (Producción y Desarrollo)
urlpatterns = [
    # Panel de control nativo de Django (Ruta ofuscada por seguridad)
    path('portal-maestro-volt/', admin.site.urls),

    # Aquí irán las futuras conexiones y delegacion de responsabilidad de cada apps de manejar cada peticion HTTP que vaya dirigida hacia la app(comentadas por ahora):
    # path('api/v1/master/', include('apps.admin.admin_users.urls')),
    # path('api/v1/tenant/', include('apps.tenant.tenant_users.urls')),
]

# Rutas que SOLO existen en la computadora de los desarrolladores
# Si en AWS el DEBUG está en False, estas rutas simplemente no se crean.
if settings.DEBUG:
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'), 
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), 
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), 
    ]