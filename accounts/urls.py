from django.urls import path
from .views import LoginApiView
from rest_framework_simplejwt.views import (
    
    TokenRefreshView, TokenObtainPairView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginApiView.as_view(), name='login'),
]