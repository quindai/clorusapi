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
    campaign_details = CampaignMetaDetailSerializer(many=True)
    class Meta:
        model = Campaign
        fields = '__all__'

    def create(self, validated_data):
        campaign_details = validated_data.pop('campaign_details')
        campaign_instance = Campaign.objects.create(**validated_data)
        obj = [CampaignMetaDetail.objects.create(**details) for details in campaign_details]
        campaign_instance.campaign_details.add(*obj)
        return campaign_instance
        
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