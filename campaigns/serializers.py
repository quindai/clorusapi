from rest_framework import serializers
from .models import Campaign
from comercial.serializers import ComercialSerializer

class CampaignSerializer(serializers.ModelSerializer):
    comercial = ComercialSerializer()
    class Meta:
        model = Campaign
        fields = '__all__'

