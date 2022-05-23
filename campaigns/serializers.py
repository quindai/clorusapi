from rest_framework import serializers

from company.serializers import CompanySerializer
from .models import Campaign, CampaignMetaDetail, Optimization
from comercial.serializers import ComercialSerializer

class CampaignSerializer(serializers.ModelSerializer):
    # comercial = ComercialSerializer()
    status = serializers.CharField()
    # company = CompanySerializer()
    comercial = ComercialSerializer()
    class Meta:
        model = Campaign
        fields = '__all__'

class CampaignMetaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignMetaDetail
        fields = '__all__'

class CampaignPostSerializer(serializers.ModelSerializer):
    last_change = serializers.DateTimeField(read_only=True)
    campaign_details = CampaignMetaDetailSerializer()
    class Meta:
        model = Campaign
        fields = '__all__'
        
class CampaignOptimizationSerializer(serializers.ModelSerializer):
    # campaign = serializers.IntegerField()
    class Meta:
        model = Optimization
        fields = '__all__'

class CampaignOptimizationGETSerializer(serializers.ModelSerializer):
    campaign_id = serializers.IntegerField()
    class Meta:
        model = Optimization
        fields = '__all__'