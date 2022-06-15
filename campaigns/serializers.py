from rest_framework import serializers

from accounts.models.apiuser import APIUser

from .models import Campaign, CampaignMetaDetail, Criativos, Optimization
from company.serializers import CompanySerializer

class CampaignMetaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignMetaDetail
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    metrics_summary = serializers.CharField()
    goal = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    campaign_details = CampaignMetaDetailSerializer(many=True)
    class Meta:
        model = Campaign
        fields = '__all__'

    def get_goal(self,obj):
        return dict(Campaign.GOAL_SELECT)[obj.goal]

    def get_year(self, obj):
        return obj.date_created.strftime('%Y')

    def get_month(self, obj):
        return obj.date_created.strftime('%b')

class CampaignPostSerializer(serializers.ModelSerializer):
    last_change = serializers.DateTimeField(read_only=True)
    campaign_details = CampaignMetaDetailSerializer(many=True)
    company = CompanySerializer(read_only=True)
    class Meta:
        model = Campaign
        fields = '__all__'

    def create(self, validated_data):
        campaign_details = validated_data.pop('campaign_details')

        active_company =  APIUser.objects.get(user=self.context['request'].user).active_company
        validated_data['company'] = active_company
        campaign_instance = Campaign.objects.create(**validated_data)
        
        # campaign_instance.company = active_company
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
    result_type = serializers.SerializerMethodField()
    class Meta:
        model = Optimization
        fields = '__all__'

    def get_result_type(self, obj):
        return dict(Optimization.DETAIL_RESULT)[obj.result_type]

class CriativoSerializer(serializers.ModelSerializer):
    metrics_summary = serializers.CharField(read_only=True)
    class Meta:
        model = Criativos
        fields = '__all__'
        #fields = ('campaign', 'ad_group_id', 'ad_id', 'description', 'tipo_midia', 'goal', 'channel', 'format','metrics_summary')