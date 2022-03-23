from django.urls import path
from .views import ComercialAPIView

urlpatterns = [
    path('', ComercialAPIView.as_view(), name='get_comercial')
]