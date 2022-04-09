from django.urls import path
from .views import CampaignAssignView, CampaignView, CampaignOptimizationView

urlpatterns = [
    path('', CampaignAssignView.as_view(), name='campaign_save'),
    path('raw_data/', CampaignView.as_view(), name='campaign'), 
    path('optimization/', CampaignOptimizationView.as_view(), name='campaign_opt'), 
]