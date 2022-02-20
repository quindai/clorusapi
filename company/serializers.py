from email.policy import default
from rest_framework import serializers
from .models import Company
from accounts.serializers import UserAPISerializer

class CompanySerializer(serializers.ModelSerializer):
    # user = UserAPISerializer(read_only=True)
    cnpj = serializers.CharField(default=None, read_only=True)
    name = serializers.CharField(default=None, read_only=True)
    logo = serializers.CharField(default=None, read_only=True)
    db_name = serializers.CharField(default=None, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'

