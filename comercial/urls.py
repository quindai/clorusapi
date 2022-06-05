from django.urls import path
from .views import ComercialAPIView, ComercialDetailsView, ComercialProductUpdateView

urlpatterns = [
    path('', ComercialAPIView.as_view(), name='get_comercial'),
    # path('<id>/', ComercialAPIView.as_view(), name='put_comercial'),
    path('<id>/product/', ComercialProductUpdateView.as_view(), name='get_comercial_products'),
    path('raw_data/', ComercialDetailsView.as_view(), name='get_products'),
]