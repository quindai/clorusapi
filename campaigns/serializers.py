from rest_framework import serializers
from .models import Campaign, Optimization
from comercial.serializers import ComercialSerializer

class CampaignSerializer(serializers.ModelSerializer):
    # comercial = ComercialSerializer()
    class Meta:
        model = Campaign
        fields = '__all__'


class CampaignOptimizationSerializer(serializers.ModelSerializer):
    # campaign = CampaignSerializer()
    class Meta:
        model = Optimization
        fields = '__all__'