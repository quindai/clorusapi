import datetime, json
from decouple import config
from itertools import islice
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import NotFound

from mysql.connector import errorcode
import mysql.connector
import decimal #for decimal field

from company.models import Company, CustomQuery
from accounts.models.apiuser import APIUser
from clorusapi.utils.common import CommonProduct
from clorusapi.utils.properties import lazy_property

from .campaign import Campaign

    # def get_queryset(self, *args, **kwargs):
    #     breakpoint()
    #     return super().get_queryset(*args, **kwargs).annotate(
            
    #     )

class Criativos(models.Model):
    GOAL_SELECT = [
        ('1','Tráfego'),
        ('2','Reconhecimento de marca'),
        ('3','Engajamento'),
        ('4','Geração de lead'),
        ('5','Vendas'),
    ]
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE) 
    ad_group_id = models.CharField(max_length=100, null=True, blank=True)  
    ad_id = models.CharField(max_length=100, null=True, blank=True)    
    description = models.CharField(max_length=255, null=True, blank=True)
    tipo_midia = models.CharField(max_length=100, null=True, blank=True)    #read_only
    
    objective = models.CharField(max_length=100, null=True, blank=True)
    channel = models.CharField(max_length=100, null=True, blank=True)   #read_only
    format = models.CharField(max_length=100, null=True, blank=True)    #read_only
    range_goal = models.IntegerField(null=True, blank=True)
    ctr_goal = models.FloatField(null=True, blank=True) #read_only
    click_goal = models.IntegerField(null=True, blank=True) #read_only
    cpc_goal = models.FloatField(null=True, blank=True) #read_only
    cpl_goal = models.FloatField(null=True, blank=True) #read_only
    cpv_goal = models.FloatField(null=True, blank=True) #read_only
    view_goal = models.FloatField(null=True, blank=True) #read_only
    leads_goal = models.FloatField(null=True, blank=True)
    invested_goal = models.FloatField(null=True, blank=True) # spend
    #metrics
    ## alcance, ctr, cliques, cpc, cpl, leads, investimento

    # objects = CriativoManager()

    def calcm(self, stmt, metric, cnx):
        with cnx.cursor(buffered=True, dictionary=True) as cursor:  
                cursor.execute(stmt)
                row = cursor.fetchone()
                cursor.close()
        return row
        
    @property
    def get_mm(self):
        # breakpoint()
        campaign = Campaign.objects.filter(pk=self.campaign.pk)
        metrics=['range','ctr','clicks','cpc','cpl','leads','invested']
        metrics_summary = {dict(MainMetrics.METRICS)[x]:None for x in metrics}
        if campaign.exists():
            q = campaign[0].custom_query
            cnx=mysql.connector.connect(
                user=config('MYSQL_DB_USER'),
                password=config('MYSQL_DB_PASS'),
                host=config('MYSQL_DB_HOST'),
                database=q.db_name)
            stmt = """SELECT CAST(SUM(Clicks) as SIGNED) as {} 
                FROM {} 
                WHERE Campaign LIKE '%{}%' AND `Ad ID`={}
                """.format(
                    dict(MainMetrics.METRICS)['clicks'],
                    '_'.join([q.company_source, 'googleads']),
                    campaign[0].clorus_id,
                    self.ad_id
                )
            col_name = dict(MainMetrics.METRICS)['clicks']
            metrics_summary[col_name] = self.calcm(stmt, 'clicks', cnx).get(col_name,None)

            stmt = """SELECT CAST(NULLIF(SUM(reach),0) as SIGNED) as {} 
                FROM {} 
                WHERE campaign_name LIKE '%{}%' AND `ad_id`={}
                """.format(
                    dict(MainMetrics.METRICS)['clicks'],
                    '_'.join([q.company_source, 'facebookads']),
                    campaign[0].clorus_id,
                    self.ad_id
                )
            col_name = dict(MainMetrics.METRICS)['range']
            metrics_summary[col_name] = self.calcm(stmt, 'range', cnx).get(col_name, None)
            cnx.close()
            return json.dumps(metrics_summary)
        return json.dumps({'metrics':[]})

    class Meta:
        ordering = ['id']

def save_criativos(instance):
    clorus_id = instance.clorus_id
    query = instance.custom_query
    cnx=mysql.connector.connect(
        user=config('MYSQL_DB_USER'),
        password=config('MYSQL_DB_PASS'),
        host=config('MYSQL_DB_HOST'),
        database=query.db_name)

    # remove espaço em branco de todos os itens separados por vírgula
    data_columns = [t.strip() for t in tuple(query.data_columns.split(',')) if t]

    # TODO colocar os criativos de todas as tabelas
    stmt = "SELECT * FROM {} WHERE {} LIKE '%{}%' GROUP BY `{}`".format(
        '_'.join([query.company_source, query.datasource]),
        data_columns[0],
        clorus_id,
        data_columns[1],
    )

    with cnx.cursor(buffered=True, dictionary=True) as cursor:  
        cursor.execute(stmt)
        rows = cursor.fetchall()
        cursor.close()
    cnx.close()

    criativos = (Criativos(
        ad_group_id= row.get('Ad group ID',''),
        ad_id= row[data_columns[1].replace('`','')],
        description= row.get('Description',''),
        tipo_midia= row['tipo_midia'],
        channel= row['channel'],
        format= row['format'],
        objective= row.get('objective',''), 
        campaign= instance
    ) for row in rows)

    batch_size = 100
    while True:
        batch = list(islice(criativos, batch_size))
        if not batch:
            break
        Criativos.objects.bulk_create(batch, batch_size)
 

@receiver(post_save, sender=Campaign)
def pre_save_handler(sender, **kwargs):
#     """after saving Campaign, update last_change"""
    instance = kwargs.get('instance')
    Campaign.objects.filter(pk=instance.pk).update(last_change = timezone.now())
    save_criativos(instance)
