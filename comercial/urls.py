from django.urls import path
from .views import ComercialAPIView, ComercialDetailsView

urlpatterns = [
    path('', ComercialAPIView.as_view(), name='get_comercial'),
    path('products/', ComercialDetailsView.as_view(), name='get_products'),
]