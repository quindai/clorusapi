from wsgiref import validate
from attr import attr
from django.forms import IntegerField
from rest_framework import serializers
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
# from accounts.models.person import Person

from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .models import APIUser, User

class UserAPISerializer(serializers.Serializer):
    class Meta:
        model = APIUser
        fields = ['email']

class LoginAPISerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=100, min_length=1, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    token = serializers.CharField(max_length=255, min_length=3, read_only=True)
    user_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=get_user_model
        fields=['email','password','username','token','user_type']

    def get_user_type(self, obj):
        return APIUser.objects.get(user__email=obj['email']).user_type

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

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token':'Token expirou ou está inválido. Por favor contacte o admin.'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    data = serializers.DictField(read_only=True)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
            # breakpoint()
            # email = attrs['data'].get('email','')
            email = attrs.get('email','')
            if APIUser.objects.filter(user__email=email).exists():
                # send email
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token= PasswordResetTokenGenerator().make_token(user)
                # current_site = get_current_site(
                    # request=attrs['data'].get('request')).domain
                current_site = 'localhost:8000'

                relative_link = reverse('reset_password_confirm', kwargs={'uidb64': uidb64, 'token':token})
                abs_url = f'http://{current_site}{relative_link}'
                send_mail(
                    subject='BI Clorus - Recuperar senha',
                    message=f'Oi {user.username} \n Use o link a seguir para redefinir a sua senha: \n{abs_url}',
                    from_email='bi@clorus.com',
                    recipient_list=[email],
                    fail_silently=False)
            return super().validate(attrs)

class PasswordTokenCheckSerializer(serializers.Serializer):
    class Meta:
        model = get_user_model
        fields = ['id']
    
    def validate(self, attrs):
        # try:
        #     id = smart_str(urlsafe_base64_decode(uidb64))
        #     user = User.objects.get(id=id)
        #     if not PasswordResetTokenGenerator().check_token(user, token):
        #         return Response({'error': 'Token não é válido.'}, status=status.HTTP_403_FORBIDDEN)

        #     ret = {'success':True,'message':'Credenciais válidas.','uidb64':uidb64, 'token':token}
        #     return Response(ret, status=status.HTTP_202_ACCEPTED)
        # except DjangoUnicodeDecodeError as e:
        #     return Response({'error': 'Token não é válido.'}, status=status.HTTP_403_FORBIDDEN)
        return super().validate(attrs)

class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(
        min_length=8, max_length=68, write_only=True)
    token=serializers.CharField(
        min_length=1, write_only=True)
    uidb64=serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password','token','uidb64']

    def validate(self, attrs):
        
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('O token é inválido', 401)
            
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed('O token é inválido', 401)

# class StarCompanyInternSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = APIUser
#         fields = ['id','star_companies']

#     def validate(self, attrs):
#         return super().validate(attrs)