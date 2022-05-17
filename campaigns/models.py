import datetime
from decouple import config
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from comercial.models import Comercial
from django.utils import timezone

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from mysql.connector import errorcode
import mysql.connector

from company.models import Company, CustomQuery
from accounts.models.apiuser import APIUser
from rest_framework.exceptions import NotFound

# TODO 
# reverse search em custom_query->company->custom_metric 
# SELECT SUM(impressions), id_clorus FROM test.sebraeal_programatica where id_clorus='#238470';

# TODO Soh retorne métricas que estão no banco de dados
class MainMetrics():
    METRICS = [ # Nome de todas as métricas
        ('impressions','Impressões'),
        ('clicks','Cliques'),
        ('range','Alcance'),
        ('views','Views de Vídeo/Áudio'),
        ('views_25','25% Views de Vídeo/Áudio'),
        ('views_50','50% Views de Vídeo/Áudio'),
        ('views_75','75% Views de Vídeo/Áudio'),
        ('views_100','100% Views de Vídeo/Áudio'),
        ('10','Conversões'),
        ('ctr','CTR - Taxa de Cliques'),
        ('cpv','CPV - Custo por View'),
        ('cpc','CPC - Custo por Clique'),
        ('cpl','CPL - Custo por lead'),
        ('visits','Visitas'),
        ('deals','Vendas'),
        ('revenue','Receita'),
        ('spend','Custo (Spend ou Investido)'),
        ('leads','Leads'),
        ('invested','Investimento / Investido'),
    ]
    METRICS_DB = [ # métricas de soma
        ('impressions',['impressions']),
        ('clicks',['clicks']),
        ('range',['reach']),
        ('views',['video_p25_watched_views', 'video_views']),
        ('views_25',['video_p25_watched_views', 'video_quartile_p25_rate', 'Twentyfive_Percent_View']),
        ('views_50',['video_p50_watched_views', 'video_quartile_p50_rate', 'Fifty_Percent_View']),
        ('views_75',['video_p75_watched_views', 'video_quartile_p75_rate', 'Seventyfive_Percent_View']),
        ('views_100',['video_p100_watched_views', 'video_quartile_p100_rate', 'Completed_view']),
        ('spend',['spend', 'Cost']),
        ('leads',['conversion']),
        # ('deals',['deals_id']),
        # ('revenue',['price']),
    ]
    # Métricas que dependem de outras métricas para serem calculadas
    METRICS_DB_ANNOTATE = [
        'ctr',
        'cpc',
        'cpv',
        'cpl',
        # 'visits',
    ]
    METRICS_API_KEY = [
        'impressions',
        'clicks',
        'range',
        'views_25',
        'views_50',
        'views_75',
        'views_100',
        'spend',
        'leads',
    ]
    METRICS_CRM = [
        'revenue'
    ]

    def get_db_table(cls, **kwargs):
        return dict(cls.METRICS_DB)[kwargs['metric']]

    def calc_annotate(metric, human_metric, *args):
        return {
            'ctr': {human_metric: args[0]/args[1]},
            'cpc': {human_metric: args[0]/args[1]},
            'cpv': {human_metric: args[0]/args[1]},
            'cpl': {human_metric: args[0]/args[1]},
        }.get(metric)

    def calc_catering(metric):
        return {
            'ctr': ['impressions','clicks'],
            'cpc': ['spend','clicks'],
            'cpv': ['spend','views'],
            'cpl': ['spend','leads'],
        }.get(metric)

    @classmethod
    def calc_metric(cls, metric, queries, clorus_id, cnx=None):
        metrics_summary = {}
        
        if metric in cls.METRICS_DB_ANNOTATE:
            metrics = cls.calc_catering(metric)
        elif metric not in [*cls.METRICS_API_KEY, *cls.METRICS_DB_ANNOTATE, 'all']:
            raise NotFound(
                _(f'{metric} métrica não existe, ou não foi mapeada.')
            )
        else:
            metrics = cls.METRICS_API_KEY if metric=='all' else [metric]
        # breakpoint()
        for q in queries:
            if not cnx:
                cnx=mysql.connector.connect(
                    user=config('MYSQL_DB_USER'),
                    password=config('MYSQL_DB_PASS'),
                    host=config('MYSQL_DB_HOST'),
                    database=q.db_name)
            # breakpoint()
            for m in metrics:
                for col in cls.get_db_table(cls, metric=m):
                    stmt = "SHOW COLUMNS FROM {} LIKE '{}'".format(
                        '_'.join([q.company_source, q.datasource]),
                        col
                    )
                    # if column exists
                    with cnx.cursor(buffered=True) as cursor:  
                        cursor.execute(stmt)
                        row = cursor.fetchone()
                        cursor.close()
                        if row:
                            stmt = "SELECT  CAST(SUM({}) AS SIGNED) as '{}' FROM {} WHERE id_clorus like '{}'".format(
                                col, 
                                dict(cls.METRICS)[m],
                                '_'.join([q.company_source, q.datasource]),
                                clorus_id
                            )
                            with cnx.cursor(buffered=True, dictionary=True) as cursor:  
                                cursor.execute(stmt)
                                row = cursor.fetchone()
                                col_name = dict(cls.METRICS)[m]
                                if col_name in metrics_summary.keys():
                                    metrics_summary[col_name] = metrics_summary[col_name]+row[col_name]
                                else:
                                    metrics_summary.update(row)
                                cursor.close()
        cnx.close()
        if metric in cls.METRICS_DB_ANNOTATE:
            # breakpoint()
            return cls.calc_annotate(
                metric,
                dict(cls.METRICS)[metric],
                metrics_summary[dict(cls.METRICS)[metrics[0]]], 
                metrics_summary[dict(cls.METRICS)[metrics[1]]]
                )
        return metrics_summary

class CampaignManager(models.Manager):
    def get_recent_date(self, *args):
        try:
            cnx=mysql.connector.connect(
                user=config('MYSQL_DB_USER'),
                password=config('MYSQL_DB_PASS'),
                host=config('MYSQL_DB_HOST'),
                database=args[0].db_name) 
            stmt = "SELECT MAX(date) as date FROM {} WHERE id_clorus like '{}' HAVING MAX(date)".format(
                '_'.join([args[0].company_source, args[0].datasource]),
                args[1])
        
            with cnx.cursor(buffered=True) as cursor:  
                cursor.execute(stmt)
                row = cursor.fetchone()
                cursor.close()

            temp_date = datetime.datetime.strptime(row[0], '%Y-%d-%m')
            if temp_date <= datetime.datetime.now()-datetime.timedelta(days=30):
                retorno = 'Inativa'
            elif temp_date < datetime.datetime.now()-datetime.timedelta(days=15):
                retorno = 'Pausada'
            else: retorno = 'Ativa'
        except mysql.connector.errors.ProgrammingError as error:
            raise ValidationError(error)
        else:
            return retorno
        finally:
            cnx.close()


    def get_metrics_sum(self, **kwargs):
        # TODO transferir para class de métricas
        metrics_summary = {}
        for q in kwargs['queries']:
            cnx=mysql.connector.connect(
                user=config('MYSQL_DB_USER'),
                password=config('MYSQL_DB_PASS'),
                host=config('MYSQL_DB_HOST'),
                database=q.db_name)
            # breakpoint()
            for m in kwargs['metrics']:
                for col in m.get_db_table(): 
                    stmt = "SHOW COLUMNS from {} LIKE '{}'".format(
                        '_'.join([q.company_source, q.datasource]),
                        col
                    )
                    # if column exists
                    with cnx.cursor(buffered=True) as cursor:  
                        cursor.execute(stmt)
                        row = cursor.fetchone()
                        cursor.close()
                    if row:
                        stmt = "SELECT  CAST(SUM({}) AS SIGNED) as {} FROM {} WHERE id_clorus like '{}'".format(
                            col, 
                            dict(m.DETAIL_METRICS)[m.id_name],
                            '_'.join([q.company_source, q.datasource]),
                            kwargs['id_clorus']
                        )
                        with cnx.cursor(buffered=True, dictionary=True) as cursor:  
                            cursor.execute(stmt)
                            row = cursor.fetchone()
                            # breakpoint()
                            if col in metrics_summary.keys():
                                metrics_summary[col] = metrics_summary[col]+row[col]
                            else:
                                metrics_summary.update(row)
                            cursor.close()
                    else: # métricas calculadas
                        pass
            cnx.close()
        # breakpoint()
        return str(metrics_summary)

    def get_calc_metric(self, metric):
        # métricas calculadas
        return {
            #CPC - Custo por Clique: f"select sum(cost)/NULLIF(SUM(clicks), 1) as CPC from test.sebraeal_facebookads;"
            'Leads': "SELECT SUM({}) as Leads FROM {}",
            'Revenue':f"select sum(cost)/NULLIF(SUM(clicks), 1) as CPC from test.sebraeal_facebookads;",
            'ROAS':f"select sum(cost)/NULLIF(SUM(clicks), 1) as CPC from test.sebraeal_facebookads;",
            'CAC':f"select sum(cost)/NULLIF(SUM(clicks), 1) as CPC from test.sebraeal_facebookads;"
        }.get(metric)
        
    def get_metrics_campaign(self, **kwargs):
        metrics_summary = {}
        for q in kwargs['queries']:
            cnx=mysql.connector.connect(
                user=config('MYSQL_DB_USER'),
                password=config('MYSQL_DB_PASS'),
                host=config('MYSQL_DB_HOST'),
                database=q.db_name)
            
            for m in kwargs['metrics']:
                if m == "Leads":
                    stmt = "SHOW COLUMNS from {} LIKE '{}'".format(
                        '_'.join([q.company_source, q.datasource]),
                        'conversions'
                    )
                    with cnx.cursor(buffered=True) as cursor:  
                        cursor.execute(stmt)
                        row = cursor.fetchone()
                        cursor.close()
                    if row:
                         stmt = "SELECT SUM(conversions) as {} FROM {}".format(
                            m,
                            '_'.join([q.company_source, q.datasource]),
                         )
                elif m == "Revenue":
                    stmt = "SHOW COLUMNS from {} LIKE '{}'".format(
                        '_'.join([q.company_source, q.datasource]),
                        'conversions'
                    )
                elif m == "ROAS":
                    stmt = "SHOW COLUMNS from {} LIKE '{}'".format(
                        '_'.join([q.company_source, q.datasource]),
                        'conversions'
                    )
                elif m == "CAC":
                    stmt = "SHOW COLUMNS from {} LIKE '{}'".format(
                        '_'.join([q.company_source, q.datasource]),
                        'conversions'
                    )

                with cnx.cursor(buffered=True, dictionary=True) as cursor:  
                    cursor.execute(stmt)
                    row = cursor.fetchone()
                    # breakpoint()
                    if m in metrics_summary.keys():
                        metrics_summary[m] = metrics_summary[m]+row[m]
                    else:
                        metrics_summary.update(row)
                    cursor.close()
                    
            cnx.close()
        return str(metrics_summary)

    def get_queryset_with_status(self, *args, **kwargs):
        retorno = self.filter(
            custom_query__company=
            APIUser.objects.get(user=args[0]).active_company
            )
        tempcq = CustomQuery.objects.get(pk=retorno[0].custom_query_id)
        
        # pega todos custom_query e busca as métricas em todos para somar
        queries = retorno[0].custom_query.company.company_rel.filter(query_type='1')
        metrics = retorno[0].custom_query.company.custommetrics_set.all()
        
        return retorno.annotate(
            # metrics_summary = models.Value(
            #     self.get_metrics_sum(metrics=metrics, queries=queries, id_clorus=retorno[0].clorus_id)),
            metrics_summary = models.Value(
                self.get_metrics_campaign(metrics=['Leads', 'Revenue','ROAS','CAC'], queries=queries, id_clorus=retorno[0].clorus_id)),
            status = models.Value(self.get_recent_date(
                tempcq, retorno[0].clorus_id
            ))
        )

class Campaign(models.Model):
    GOAL_SELECT = [
        ('1','Tráfego'),
        ('2','Reconhecimento de marca'),
        ('3','Engajamento'),
        ('4','Geração de lead'),
        ('5','Vendas'),
    ]
    clorus_id = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='', verbose_name="Nome da Campanha")
    image = models.TextField(default='')
    goal = models.CharField(max_length=2, default='', choices=GOAL_SELECT, 
                            verbose_name="Objetivo da Campanha", help_text='')
    goal_description = models.TextField(default='', verbose_name="Descrição do Objetivo")
    goal_budget = models.CharField(max_length=255, default='', verbose_name='Meta (Total proveniente de Meta Geral)')
    comercial = models.ForeignKey(Comercial, on_delete=models.CASCADE, default=1)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    custom_query = models.ForeignKey(CustomQuery, on_delete=models.CASCADE)
    budget = models.CharField(max_length=255, default='', verbose_name="Valor Investido")
    last_change = models.DateTimeField(blank=True, null=True)

    objects = CampaignManager()

    class Meta:
        ordering = ['id']

@receiver(post_save, sender=Campaign)
def pre_save_handler(sender, **kwargs):
#     """after saving Campaign, update last_change"""
    instance = kwargs.get('instance')
    Campaign.objects.filter(pk=instance.pk).update(last_change = timezone.now())

class Optimization(models.Model):
    DETAIL_RESULT = [
        ('1','Negativo'),
        ('2','Positivo'),
        ('3','Neutro')
    ]
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, db_index=True)
    description = models.TextField()
    hypothesis = models.TextField()
    result = models.TextField()
    result_type = models.CharField(max_length=2, choices=DETAIL_RESULT)

    class Meta:
        ordering = ['date']