from django.contrib import admin
from .models import Campaign, Criativos, Optimization, CampaignMetaDetail
# Register your models here.

class CampaignAdmin(admin.ModelAdmin):
    list_filter = ('company',)

admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Optimization)
admin.site.register(CampaignMetaDetail)
admin.site.register(Criativos)