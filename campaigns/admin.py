from django.contrib import admin
from .models import Campaign, Optimization, CampaignMetaDetail
# Register your models here.

admin.site.register(Campaign)
admin.site.register(Optimization)
admin.site.register(CampaignMetaDetail)