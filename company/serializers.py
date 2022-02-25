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

class StarCompanyInternSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=None)
    class Meta:
        model = Company
        fields = '__all__'

    def validate_id(self, value):
        if(value is None):
            raise serializers.ValidationError("Valor de id não informado")
        return value

    def validate(self, attrs):

        return super().validate(attrs)