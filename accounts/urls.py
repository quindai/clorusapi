from django.urls import path
# from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# router = DefaultRouter()
# router.register(r'auth/token/', TokenObtainPairView, basename='token_obtain_pair')
# router.register(r'auth/token/refresh/', TokenRefreshView, basename='token_refresh')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]