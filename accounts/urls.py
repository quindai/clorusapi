from django.urls import path
from .views import LoginAPIView, LogoutAPIView, PasswordTokenCheckAPI, RequestPasswordResetEmailView, SetNewPasswordAPIView
from rest_framework_simplejwt.views import (
    
    TokenRefreshView, TokenObtainPairView
)

urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='auth_logout'),
    path('reset-password/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='reset_password_confirm'),
    path('request-reset-password/', RequestPasswordResetEmailView.as_view(), name='request-reset-password'),
    path('reset-password-complete', SetNewPasswordAPIView.as_view(),name='reset-password-complete'),

]