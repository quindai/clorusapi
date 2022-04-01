from django.urls import path
from .views import CampaignAssignView, CampaignView

urlpatterns = [
    path('raw_data/', CampaignView.as_view(), name='campaign'),    
    path('', CampaignAssignView.as_view(), name='campaign_save'),
]