import email
from rest_framework import serializers
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
# from accounts.models.person import Person

from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .models import APIUser

class UserAPISerializer(serializers.Serializer):
    class Meta:
        model = APIUser
        fields = ['email']

class LoginAPISerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=100, min_length=1, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    token = serializers.CharField(max_length=255, min_length=3, read_only=True)

    class Meta:
        model=get_user_model
        fields=['email','password','username','token']

    def validate(self, value):
        email=value.get('email','')
        password=value.get('password','')
        user=auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials.')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin.')
        return {
            'email': user.email,
            'username': user.username,
            'token': user.get_tokens_for_user
        }
        # return super().validate(value)

