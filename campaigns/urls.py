from django.urls import path
from .views import CampaignView

urlpatterns = [
    path('', CampaignView.as_view(), name='campaign'),    

]