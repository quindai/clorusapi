from rest_framework import serializers
from .models import Comercial

class ComercialSerializer(serializers.ModelSerializer):
    _begin_date = serializers.DateField(read_only=True)
    class Meta:
        model = Comercial
        fields = '__all__'