from accounts.models.apiuser import APIUser
from rest_framework import serializers
from .models import Company, CustomMetrics, CustomQuery

class CustomQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomQuery
        fields = '__all__'

class CustomMetricsSerializer(serializers.ModelSerializer):
    # name=serializers.SerializerMethodField('get_db_table')
    friendly_name=serializers.ReadOnlyField(source='__str__')
    name=serializers.ReadOnlyField(source='get_db_table')
    class Meta:
        model = CustomMetrics
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    cnpj = serializers.CharField(default=None, read_only=True)
    name = serializers.CharField(default=None, read_only=True)
    logo = serializers.CharField(default=None, read_only=True)
    funil_metrics = serializers.ListSerializer(
        child=CustomMetricsSerializer(), 
        source='custommetrics_set')

    class Meta:
        model = Company
        fields = '__all__'


class CompanyInternSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=None)
    funil = serializers.ListSerializer(
        child=CustomMetricsSerializer(), 
        source='custommetrics_set')
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('cnpj','name','logo', 'funil')
        extra_kwargs = {
            'id': {'write_only': True},
        }
