"""clorusapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
#router.register(r'route', MyViewSet, basename='View Namce')

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Clorus API",
      default_version='v1',
      description="API de uso interno para construção de aplicações WEB/Mobile.",
      terms_of_service="/",
      contact=openapi.Contact(email="randy.quindai@gmail.com"),
      license=openapi.License(name="Local License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('company/', include('company.urls')),
    path('comercial/', include('comercial.urls')),
    path('campaign/', include('campaigns.urls')),
    # path('company/<int:pk>/', UpdateCompanyAPIView.as_view(), name='update_company'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api.json/', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
]
