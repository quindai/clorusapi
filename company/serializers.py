from rest_framework import serializers
from .models import Company
from accounts.serializers import UserAPISerializer

class CompanySerializer(serializers.Serializer):
    user = UserAPISerializer(read_only=True)
    class Meta:
        model = Company
        fields = ('cnpj','name')