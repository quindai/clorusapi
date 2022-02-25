# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DrvisOptyGoogleads(models.Model):
    day = models.DateField(blank=True, null=True)
    campaign_id = models.TextField(db_column='Campaign ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    campaign = models.TextField(db_column='Campaign', blank=True, null=True)  # Field name made lowercase.
    ad_group_id = models.TextField(db_column='Ad group ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ad_id = models.TextField(db_column='Ad ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    image_ad_url = models.TextField(db_column='Image Ad URL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    image_ad_name = models.TextField(db_column='Image ad name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    display_url = models.TextField(db_column='Display URL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    impressions = models.IntegerField(db_column='Impressions', blank=True, null=True)  # Field name made lowercase.
    clicks = models.IntegerField(db_column='Clicks', blank=True, null=True)  # Field name made lowercase.
    conversions = models.FloatField(db_column='Conversions', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'drvis_opty_googleads'


class FaculdadeNegociosFanFacebookads(models.Model):
    account_currency = models.CharField(max_length=3, blank=True, null=True)
    account_id = models.TextField(blank=True, null=True)
    account_name = models.TextField(blank=True, null=True)
    ad_id = models.TextField(blank=True, null=True)
    ad_name = models.TextField(blank=True, null=True)
    adset_id = models.TextField(blank=True, null=True)
    adset_name = models.TextField(blank=True, null=True)
    campaign_id = models.TextField(blank=True, null=True)
    cpp = models.FloatField(blank=True, null=True)
    ctr = models.FloatField(blank=True, null=True)
    day = models.DateField(blank=True, null=True)
    frequency = models.FloatField(blank=True, null=True)
    impressions = models.IntegerField(blank=True, null=True)
    objective = models.TextField(blank=True, null=True)
    reach = models.IntegerField(blank=True, null=True)
    social_spend = models.FloatField(blank=True, null=True)
    spend = models.FloatField(blank=True, null=True)
    unique_clicks = models.IntegerField(blank=True, null=True)
    unique_ctr = models.FloatField(blank=True, null=True)
    video_30_sec_watched_views = models.IntegerField(blank=True, null=True)
    video_p100_watched_views = models.IntegerField(blank=True, null=True)
    video_p25_watched_views = models.IntegerField(blank=True, null=True)
    video_p50_watched_views = models.IntegerField(blank=True, null=True)
    video_p75_watched_views = models.IntegerField(blank=True, null=True)
    video_p95_watched_views = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculdade_negocios_fan_facebookads'


class HobOptyGoogleads(models.Model):
    day = models.DateField(blank=True, null=True)
    campaign_id = models.TextField(db_column='Campaign ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    campaign = models.TextField(db_column='Campaign', blank=True, null=True)  # Field name made lowercase.
    ad_group_id = models.TextField(db_column='Ad group ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ad_id = models.TextField(db_column='Ad ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    image_ad_url = models.TextField(db_column='Image Ad URL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    image_ad_name = models.TextField(db_column='Image ad name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    display_url = models.TextField(db_column='Display URL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    impressions = models.IntegerField(db_column='Impressions', blank=True, null=True)  # Field name made lowercase.
    clicks = models.IntegerField(db_column='Clicks', blank=True, null=True)  # Field name made lowercase.
    conversions = models.FloatField(db_column='Conversions', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hob_opty_googleads'


class HoslOptyFacebookads(models.Model):
    account_currency = models.CharField(max_length=3, blank=True, null=True)
    account_id = models.TextField(blank=True, null=True)
    account_name = models.TextField(blank=True, null=True)
    ad_id = models.TextField(blank=True, null=True)
    ad_name = models.TextField(blank=True, null=True)
    adset_id = models.TextField(blank=True, null=True)
    adset_name = models.TextField(blank=True, null=True)
    campaign_id = models.TextField(blank=True, null=True)
    campaign_name = models.TextField(blank=True, null=True)
    clicks = models.IntegerField(blank=True, null=True)
    conversions = models.IntegerField(blank=True, null=True)
    cpc = models.FloatField(blank=True, null=True)
    cpp = models.FloatField(blank=True, null=True)
    ctr = models.FloatField(blank=True, null=True)
    day = models.DateField(blank=True, null=True)
    frequency = models.FloatField(blank=True, null=True)
    impressions = models.IntegerField(blank=True, null=True)
    objective = models.TextField(blank=True, null=True)
    reach = models.IntegerField(blank=True, null=True)
    social_spend = models.FloatField(blank=True, null=True)
    spend = models.FloatField(blank=True, null=True)
    unique_clicks = models.IntegerField(blank=True, null=True)
    unique_ctr = models.FloatField(blank=True, null=True)
    video_30_sec_watched_views = models.IntegerField(blank=True, null=True)
    video_p100_watched_views = models.IntegerField(blank=True, null=True)
    video_p25_watched_views = models.IntegerField(blank=True, null=True)
    video_p50_watched_views = models.IntegerField(blank=True, null=True)
    video_p75_watched_views = models.IntegerField(blank=True, null=True)
    video_p95_watched_views = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hosl_opty_facebookads'


class HoslOptyGoogleads(models.Model):
    day = models.DateField(blank=True, null=True)
    campaign_id = models.TextField(db_column='Campaign ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    campaign = models.TextField(db_column='Campaign', blank=True, null=True)  # Field name made lowercase.
    ad_group_id = models.TextField(db_column='Ad group ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ad_id = models.TextField(db_column='Ad ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    image_ad_url = models.TextField(db_column='Image Ad URL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    image_ad_name = models.TextField(db_column='Image ad name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    display_url = models.TextField(db_column='Display URL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    impressions = models.IntegerField(db_column='Impressions', blank=True, null=True)  # Field name made lowercase.
    clicks = models.IntegerField(db_column='Clicks', blank=True, null=True)  # Field name made lowercase.
    conversions = models.FloatField(db_column='Conversions', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    ad_name = models.CharField(db_column='Ad Name', max_length=55, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    video_views = models.IntegerField(blank=True, null=True)
    video_quartile_p100_rate = models.IntegerField(blank=True, null=True)
    video_quartile_p25_rate = models.IntegerField(blank=True, null=True)
    video_quartile_p50_rate = models.IntegerField(blank=True, null=True)
    video_quartile_p75_rate = models.IntegerField(blank=True, null=True)
    ad_group_name = models.CharField(db_column='Ad group Name', max_length=55, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ad_type = models.CharField(db_column='Ad type', max_length=55, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'hosl_opty_googleads'


class PrevidaGoogleads(models.Model):
    day = models.DateField(blank=True, null=True)
    campaign_id = models.TextField(db_column='Campaign ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    campaign = models.TextField(db_column='Campaign', blank=True, null=True)  # Field name made lowercase.
    ad_group_id = models.TextField(db_column='Ad group ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ad_id = models.TextField(db_column='Ad ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    image_ad_url = models.TextField(db_column='Image Ad URL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    image_ad_name = models.TextField(db_column='Image ad name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    display_url = models.TextField(db_column='Display URL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    impressions = models.IntegerField(db_column='Impressions', blank=True, null=True)  # Field name made lowercase.
    clicks = models.IntegerField(db_column='Clicks', blank=True, null=True)  # Field name made lowercase.
    conversions = models.FloatField(db_column='Conversions', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'previda_googleads'


class SebraealFacebookads(models.Model):
    account_currency = models.CharField(max_length=3, blank=True, null=True)
    account_id = models.TextField(blank=True, null=True)
    account_name = models.TextField(blank=True, null=True)
    ad_id = models.TextField(blank=True, null=True)
    ad_name = models.TextField(blank=True, null=True)
    adset_id = models.TextField(blank=True, null=True)
    adset_name = models.TextField(blank=True, null=True)
    campaign_id = models.TextField(blank=True, null=True)
    campaign_name = models.TextField(blank=True, null=True)
    clicks = models.IntegerField(blank=True, null=True)
    conversions = models.IntegerField(blank=True, null=True)
    cpc = models.FloatField(blank=True, null=True)
    cpp = models.FloatField(blank=True, null=True)
    ctr = models.FloatField(blank=True, null=True)
    day = models.DateField(blank=True, null=True)
    frequency = models.FloatField(blank=True, null=True)
    impressions = models.IntegerField(blank=True, null=True)
    objective = models.TextField(blank=True, null=True)
    reach = models.IntegerField(blank=True, null=True)
    social_spend = models.FloatField(blank=True, null=True)
    spend = models.FloatField(blank=True, null=True)
    unique_clicks = models.IntegerField(blank=True, null=True)
    unique_ctr = models.FloatField(blank=True, null=True)
    video_30_sec_watched_views = models.IntegerField(blank=True, null=True)
    video_p100_watched_views = models.IntegerField(blank=True, null=True)
    video_p25_watched_views = models.IntegerField(blank=True, null=True)
    video_p50_watched_views = models.IntegerField(blank=True, null=True)
    video_p75_watched_views = models.IntegerField(blank=True, null=True)
    video_p95_watched_views = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sebraeal_facebookads'


class SebraealGoogleads(models.Model):
    day = models.DateField(blank=True, null=True)
    campaign_id = models.TextField(db_column='Campaign ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    campaign = models.TextField(db_column='Campaign', blank=True, null=True)  # Field name made lowercase.
    ad_group_id = models.TextField(db_column='Ad group ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ad_id = models.TextField(db_column='Ad ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    image_ad_url = models.TextField(db_column='Image Ad URL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    image_ad_name = models.TextField(db_column='Image ad name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    display_url = models.TextField(db_column='Display URL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    impressions = models.IntegerField(db_column='Impressions', blank=True, null=True)  # Field name made lowercase.
    clicks = models.IntegerField(db_column='Clicks', blank=True, null=True)  # Field name made lowercase.
    conversions = models.FloatField(db_column='Conversions', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    ad_name = models.CharField(db_column='Ad Name', max_length=55, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    video_views = models.IntegerField(blank=True, null=True)
    video_quartile_p100_rate = models.IntegerField(blank=True, null=True)
    video_quartile_p25_rate = models.IntegerField(blank=True, null=True)
    video_quartile_p50_rate = models.IntegerField(blank=True, null=True)
    video_quartile_p75_rate = models.IntegerField(blank=True, null=True)
    ad_group_name = models.CharField(db_column='Ad group Name', max_length=55, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ad_type = models.CharField(db_column='Ad type', max_length=55, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'sebraeal_googleads'


class SplitsecondFacebookads(models.Model):
    account_currency = models.CharField(max_length=3, blank=True, null=True)
    account_id = models.TextField(blank=True, null=True)
    account_name = models.TextField(blank=True, null=True)
    ad_id = models.TextField(blank=True, null=True)
    ad_name = models.TextField(blank=True, null=True)
    adset_id = models.TextField(blank=True, null=True)
    adset_name = models.TextField(blank=True, null=True)
    campaign_id = models.TextField(blank=True, null=True)
    campaign_name = models.TextField(blank=True, null=True)
    clicks = models.IntegerField(blank=True, null=True)
    conversions = models.IntegerField(blank=True, null=True)
    cpc = models.FloatField(blank=True, null=True)
    cpp = models.FloatField(blank=True, null=True)
    ctr = models.FloatField(blank=True, null=True)
    day = models.DateField(blank=True, null=True)
    frequency = models.FloatField(blank=True, null=True)
    impressions = models.IntegerField(blank=True, null=True)
    objective = models.TextField(blank=True, null=True)
    reach = models.IntegerField(blank=True, null=True)
    social_spend = models.FloatField(blank=True, null=True)
    spend = models.FloatField(blank=True, null=True)
    unique_clicks = models.IntegerField(blank=True, null=True)
    unique_ctr = models.FloatField(blank=True, null=True)
    video_30_sec_watched_views = models.IntegerField(blank=True, null=True)
    video_p100_watched_views = models.IntegerField(blank=True, null=True)
    video_p25_watched_views = models.IntegerField(blank=True, null=True)
    video_p50_watched_views = models.IntegerField(blank=True, null=True)
    video_p75_watched_views = models.IntegerField(blank=True, null=True)
    video_p95_watched_views = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'splitsecond_facebookads'


class SplitsecondGoogleads(models.Model):
    day = models.DateField(blank=True, null=True)
    campaign_id = models.TextField(db_column='Campaign ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    campaign = models.TextField(db_column='Campaign', blank=True, null=True)  # Field name made lowercase.
    ad_group_id = models.TextField(db_column='Ad group ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ad_id = models.TextField(db_column='Ad ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    image_ad_url = models.TextField(db_column='Image Ad URL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    image_ad_name = models.TextField(db_column='Image ad name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    display_url = models.TextField(db_column='Display URL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    impressions = models.IntegerField(db_column='Impressions', blank=True, null=True)  # Field name made lowercase.
    clicks = models.IntegerField(db_column='Clicks', blank=True, null=True)  # Field name made lowercase.
    conversions = models.FloatField(db_column='Conversions', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    ad_name = models.CharField(db_column='Ad Name', max_length=55, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    video_views = models.IntegerField(blank=True, null=True)
    video_quartile_p100_rate = models.IntegerField(blank=True, null=True)
    video_quartile_p25_rate = models.IntegerField(blank=True, null=True)
    video_quartile_p50_rate = models.IntegerField(blank=True, null=True)
    video_quartile_p75_rate = models.IntegerField(blank=True, null=True)
    ad_group_name = models.CharField(db_column='Ad group Name', max_length=55, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ad_type = models.CharField(db_column='Ad type', max_length=55, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'splitsecond_googleads'
