from ast import Try
import email
from rest_framework import serializers
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from accounts.models.person import Person
from .models import User

class RequestResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        try:
            email = attrs.get('email', '')
            if User.objects.filter(person__email=email).exists():
                user = Person.objects.get(email=email)
                uidb64=urlsafe_base64_encode(user.id)
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(self.request).domain
                relative_link = reverse('email-verify')
                full_url = 'http://'+current_site +
                send_mail(
                    subject='Definir nova senha',
                    message=f'Você requisitou mudança de senha, clica no link abaixo por favor.<br\>{token}',
                    from_email='bi@clorus.com',
                    recipient_list=[User.objects.get(person__email=email)],
                    fail_silently=False
                    )
            return attrs
        except e as identifier:
            pass
        return super().validate(attrs)