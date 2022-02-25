# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DetranProgramatica(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_view', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detran_programatica'


class DetranSocial(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    interactions = models.CharField(db_column='Interactions', max_length=50)  # Field name made lowercase.
    reactions = models.CharField(db_column='Reactions', max_length=50)  # Field name made lowercase.
    shares = models.CharField(db_column='Shares', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_View', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detran_social'


class GovAlProgramatica(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    frequency = models.CharField(db_column='Frequency', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_view', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.
    region = models.CharField(db_column='Region', max_length=50, blank=True, null=True)  # Field name made lowercase.
    unique_reach = models.CharField(db_column='Unique reach', max_length=50, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'gov_al_programatica'


class GovAlSocial(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    frequency = models.CharField(db_column='Frequency', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    interactions = models.CharField(db_column='Interactions', max_length=50)  # Field name made lowercase.
    reactions = models.CharField(db_column='Reactions', max_length=50)  # Field name made lowercase.
    shares = models.CharField(db_column='Shares', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_View', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.
    platform = models.CharField(db_column='Platform', max_length=50, blank=True, null=True)  # Field name made lowercase.
    placement = models.CharField(db_column='Placement', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'gov_al_social'


class HospitalProgramatica(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_view', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hospital_programatica'


class HospitalSocial(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    interactions = models.CharField(db_column='Interactions', max_length=50)  # Field name made lowercase.
    reactions = models.CharField(db_column='Reactions', max_length=50)  # Field name made lowercase.
    shares = models.CharField(db_column='Shares', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_View', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hospital_social'


class ImobiliariaProgramatica(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_view', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'imobiliaria_programatica'


class ImobiliariaSocial(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    interactions = models.CharField(db_column='Interactions', max_length=50)  # Field name made lowercase.
    reactions = models.CharField(db_column='Reactions', max_length=50)  # Field name made lowercase.
    shares = models.CharField(db_column='Shares', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_View', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'imobiliaria_social'


class JandjSocial(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    interactions = models.CharField(db_column='Interactions', max_length=50)  # Field name made lowercase.
    reactions = models.CharField(db_column='Reactions', max_length=50)  # Field name made lowercase.
    shares = models.CharField(db_column='Shares', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_View', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.
    survey_visits = models.CharField(db_column='Survey_Visits', max_length=50)  # Field name made lowercase.
    survey_ends = models.CharField(db_column='Survey_Ends', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'jandj_social'


class PublyaProgramatica(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_view', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'publya_programatica'


class PublyaSocial(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    interactions = models.CharField(db_column='Interactions', max_length=50)  # Field name made lowercase.
    reactions = models.CharField(db_column='Reactions', max_length=50)  # Field name made lowercase.
    shares = models.CharField(db_column='Shares', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_View', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'publya_social'


class SebraeProgramatica(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_view', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sebrae_programatica'


class SebraeSocial(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    interactions = models.CharField(db_column='Interactions', max_length=50)  # Field name made lowercase.
    reactions = models.CharField(db_column='Reactions', max_length=50)  # Field name made lowercase.
    shares = models.CharField(db_column='Shares', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_View', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sebrae_social'


class SemarhProgramatica(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_view', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'semarh_programatica'


class SemarhSocial(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    interactions = models.CharField(db_column='Interactions', max_length=50)  # Field name made lowercase.
    reactions = models.CharField(db_column='Reactions', max_length=50)  # Field name made lowercase.
    shares = models.CharField(db_column='Shares', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_View', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'semarh_social'


class SesauProgramatica(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_view', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sesau_programatica'


class SesauSocial(models.Model):
    day = models.CharField(db_column='Day', max_length=50)  # Field name made lowercase.
    advertiser_name = models.CharField(db_column='Advertiser_Name', max_length=50)  # Field name made lowercase.
    campaign = models.CharField(db_column='Campaign', max_length=50)  # Field name made lowercase.
    strategy = models.CharField(db_column='Strategy', max_length=50)  # Field name made lowercase.
    substrategy = models.CharField(db_column='Substrategy', max_length=50)  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50)  # Field name made lowercase.
    objective = models.CharField(db_column='Objective', max_length=50)  # Field name made lowercase.
    creative_format = models.CharField(db_column='Creative_Format', max_length=50)  # Field name made lowercase.
    creative_type = models.CharField(db_column='Creative_Type', max_length=50)  # Field name made lowercase.
    creative_set = models.CharField(db_column='Creative_Set', max_length=50)  # Field name made lowercase.
    impressions = models.CharField(db_column='Impressions', max_length=50)  # Field name made lowercase.
    clicks = models.CharField(db_column='Clicks', max_length=50)  # Field name made lowercase.
    interactions = models.CharField(db_column='Interactions', max_length=50)  # Field name made lowercase.
    reactions = models.CharField(db_column='Reactions', max_length=50)  # Field name made lowercase.
    shares = models.CharField(db_column='Shares', max_length=50)  # Field name made lowercase.
    completed_view = models.CharField(db_column='Completed_View', max_length=50)  # Field name made lowercase.
    twentyfive_percent_view = models.CharField(db_column='Twentyfive_Percent_View', max_length=50)  # Field name made lowercase.
    fifty_percent_view = models.CharField(db_column='Fifty_Percent_View', max_length=50)  # Field name made lowercase.
    seventyfive_percent_view = models.CharField(db_column='Seventyfive_Percent_View', max_length=50)  # Field name made lowercase.
    spend = models.CharField(db_column='Spend', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sesau_social'
