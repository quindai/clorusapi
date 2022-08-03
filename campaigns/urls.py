from django.urls import path
from .views import CampaignPostView, CampaignView, CampaignRawDataView, CampaignOptimizationView, CampaignOptimizationGETView, CriativosView

urlpatterns = [
    path('', CampaignPostView.as_view(), name='campaign_save'),
    path('list/', CampaignView.as_view(), name='campaign'),
    path('raw_data/', CampaignRawDataView.as_view(), name='campaign_raw_data'), 
    path('optimization/', CampaignOptimizationView.as_view(), name='campaign_opt'), 
    path('optimization/<campaign_id>/', CampaignOptimizationGETView.as_view(), name='campaign_opt_save'), 
    path('criativos/<campaign_id>', CriativosView.as_view(), name='criativos'),
]