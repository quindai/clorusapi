from logging import exception
from rest_framework import serializers
from rest_framework.exceptions import (
    AuthenticationFailed, PermissionDenied, NotFound)
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
# from accounts.models.person import Person

from django.contrib import auth
from django.contrib.auth import get_user_model
from .models import APIUser, User

class UserAPISerializer(serializers.Serializer):
    user_type = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, read_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    email = serializers.EmailField(max_length=255, read_only=True)

    class Meta:
        model = APIUser
        fields = '__all__'

    def validate(self, value):
        try:
            user = APIUser.objects.get(user__pk=self.initial_data['pk'])
        except APIUser.DoesNotExist:
            raise NotFound('Usuário não encontrado.')
        else:
            return {
                'user_type':user.user_type,
                'name':user.name,  
                'username':user.user.username,
                'email':user.user.email
            }

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
            raise AuthenticationFailed('Credenciais inválidas.')
        if not user.is_active:
            raise AuthenticationFailed('Conta desativada, contacte o admin.')
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
            # email = attrs['data'].get('email','')
            email = attrs.get('email','')
            # if APIUser.objects.filter(user__email=email).exists():
            try:
                # send email
                user = APIUser.objects.get(user__email=email).user
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token= PasswordResetTokenGenerator().make_token(user)
                # current_site = get_current_site(
                    # request=attrs['data'].get('request')).domain
                current_site = self.initial_data['request'].META['HTTP_REFERER']

                # rota do front
                # http://clorusanalytics.tk/passwordreset/:base64/:token

                relative_link = reverse('reset_password_confirm', kwargs={'uidb64': uidb64, 'token':token})
                abs_url = f'{current_site[:-1]}{relative_link}'
                send_mail(
                    subject='BI Clorus - Recuperar senha',
                    message=f'Oi {user.username} \n Use o link a seguir para redefinir a sua senha: \n{abs_url}',
                    from_email='bi@clorus.com',
                    recipient_list=[email],
                    fail_silently=False)
            except APIUser.DoesNotExist:
                raise NotFound({'error':'Email não cadastrado.'})
            else:
                return super().validate(attrs)

class PasswordTokenCheckSerializer(serializers.Serializer):
    class Meta:
        model = get_user_model
        fields = ['id']
    
    def validate(self, attrs):
        # breakpoint()
        try:
            uidb64=self.context.get("uidb64")
            token=self.context.get("token")
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise PermissionDenied({'error': 'Token não é válido.'})
            return super().validate({'success':True,
                    'message':'Credenciais válidas.',
                    'uidb64':uidb64, 'token':token
                    })

        #     return Response(ret, status=status.HTTP_202_ACCEPTED)
        except DjangoUnicodeDecodeError as e:
            raise PermissionDenied({'error': 'Token não é válido.'})
        # return super().validate(attrs)

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
                raise AuthenticationFailed('O token é inválido.', 401)
            
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed('O token é inválido.', 401)

# class StarCompanyInternSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = APIUser
#         fields = ['id','star_companies']

#     def validate(self, attrs):
#         return super().validate(attrs)