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

class MainMetrics():
    """
    This class returns the value of metrics.
    Guarantees that only mapped metrics are returned.
    """
    METRICS = [ # Name of all metrics
        ('impressions','Impressões'),
        ('clicks','Cliques'),
        ('range','Alcance'),
        ('views','Views de Vídeo/Áudio'),
        ('views_25','25% Views de Vídeo/Áudio'),
        ('views_50','50% Views de Vídeo/Áudio'),
        ('views_75','75% Views de Vídeo/Áudio'),
        ('views_100','100% Views de Vídeo/Áudio'),
        ('ctr','CTR - Taxa de Cliques'),
        ('cpv','CPV - Custo por View'),
        ('cpc','CPC - Custo por Clique'),
        ('cpl','CPL - Custo por lead'),
        ('visits','Visitas'),
        ('deals','Vendas'),
        ('revenue','Receita'),
        ('spend','Custo (Spend ou Investido)'),
        ('leads','Leads'),
        # ('invested','Investimento / Investido'),
        ('roas','ROAS'),
        ('cac','CAC - Custo de Aquisição de Cliente'),
        ('budget','Verba'),
        ('balance','Saldo'),
        ('invested','Investido'),
        ('conversions','Conversão'),
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
        ('deals',['id']),
        ('revenue',['price']),
        ('conversions', ['conversion'])
    ]
    # Métricas que dependem de outras métricas para serem calculadas
    METRICS_DB_ANNOTATE = [
        'ctr',
        'cpc',
        'cpv',
        'cpl',
        'roas',
        'cac',
        'balance',
        'invested',
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
        'conversions',
    ]
    METRICS_CRM = [
        'revenue',
        'deals'
    ]
    METRICS_RD = [
        'email',
        'opportunities',
        'visits',
        # 'conversions'
    ]
    METRICS_MARKETEER = [
        'budget'
    ]
    METRICS_HYBRID = [
        'balance',
        # 'invested'
    ]

    def get_db_table(cls, **kwargs):
        return dict(cls.METRICS_DB)[kwargs['metric']]

    def calc_annotate(metric, human_metric, *args):
        if args[1] == 0:
            return {human_metric: args[1]}
        try:
            return {
                'ctr': {human_metric: args[0]/args[1]},
                'cpc': {human_metric: args[0]/args[1]},
                'cpv': {human_metric: args[0] if args[1]==0 else args[0]/args[1]},
                'cpl': {human_metric: args[0]/args[1]},
                'roas': {human_metric: (args[1] - args[0])/args[0] },
                'cac': {human_metric: args[0]/args[1]},
                'balance': {human_metric: 0 if args[0]-args[1] < 0 else args[0]-args[1]},
                'invested': {human_metric: sum(args)}
            }.get(metric)
        except Exception as e:
            raise ValidationError({'error':e, 'detail':f'Métrica {human_metric} com divisor zero 0, não pode ser calculada.'})

    def calc_catering(metric):
        return {
            'ctr': ['impressions','clicks'],
            'cpc': ['spend','clicks'],
            'cpv': ['spend','views'],
            'cpl': ['spend','leads'],
            'roas': ['spend','revenue'],
            'cac': ['spend','deals'],
            'balance': ['budget','spend'],
            #TODO
            # retificar invested
            'invested': ['spend','cpc','cpv','cac','cpl'],
            'email': ['sent', 'delivered', 'opened', 'tx_opened', 'tx_clicks']
        }.get(metric)

    @classmethod
    def calc_metric(cls, metric, queries, clorus_id, product_id=None, campaigns=None, cnx=None):
        # breakpoint()
        if not 'metrics_summary' in vars():
            metrics_summary = {}
        if metric in cls.METRICS_DB_ANNOTATE:
            metrics = cls.calc_catering(metric)
        elif metric in cls.METRICS_MARKETEER:
            metrics_summary = {dict(cls.METRICS)[metric]: campaigns.aggregate(models.Sum('budget'))['budget__sum']}
            queries = [] # condition to make sure that no other metric will be calculated
        elif metric not in [*cls.METRICS_API_KEY, *cls.METRICS_RD, 'all']:
            raise NotFound(
                _(f'{metric} métrica não existe, ou não foi mapeada.')
            )
        else:
            metrics = cls.METRICS_API_KEY if metric=='all' else [metric]
        # breakpoint()
        if metric in cls.METRICS_HYBRID:
            for m in metrics:
                if dict(cls.METRICS)[m] in metrics_summary.keys():
                    metrics_summary[dict(cls.METRICS)[m]] = metrics_summary[dict(cls.METRICS)[m]] + metrics_summary.update(
                        cls.calc_metric(m, queries, clorus_id, product_id, campaigns, cnx)
                    )[dict(cls.METRICS)[m]]
                else:
                    metrics_summary.update(
                        cls.calc_metric(m, queries, clorus_id, product_id, campaigns, cnx)
                    )
        elif metric in cls.METRICS_RD:
            # breakpoint()
            for q in queries:
                if 'emails' in q.datasource and metric == 'email':
                    metrics = ['email_' + x for x in cls.calc_catering(metric)]
                    cnx=mysql.connector.connect(
                        user=config('MYSQL_DB_USER'),
                        password=config('MYSQL_DB_PASS'),
                        host=config('MYSQL_DB_HOST'),
                        database=q.db_name)
                    # stmt = "SELECT SUM({}) FROM {} WHERE {} LIKE '%{}%'"
                    stmt = """SELECT SUM(`{}`) as {}, 
                                SUM(`{}`) as {}, 
                                SUM(`{}`) as {}, 
                                SUM(`{}`) as {} 
                                FROM {}""".format(
                        'Leads selecionados',
                        'Enviados',
                        'Entregues',
                        'Entrega',
                        'Aberturas (unicas)',
                        'Abertos',
                        'Cliques (unicos)',
                        'Clicados',
                        '_'.join([q.company_source, q.datasource]),
                    )

                    with cnx.cursor(buffered=True, dictionary=True) as cursor:  
                        cursor.execute(stmt)
                        row = cursor.fetchone()
                        # col_name = dict(cls.METRICS)[m]
                        col_name = ['Enviados','Entrega','Abertos','Clicados']
                        if set(col_name).issubset(metrics_summary.keys()):
                                metrics_summary[col_name[0]] = metrics_summary[col_name[0]]+row[col_name[0]]
                                metrics_summary[col_name[1]] = metrics_summary[col_name[1]]+row[col_name[1]]
                                metrics_summary[col_name[2]] = metrics_summary[col_name[2]]+row[col_name[2]]
                                metrics_summary[col_name[3]] = metrics_summary[col_name[3]]+row[col_name[3]]
                        else:
                            metrics_summary.update(row)
                        metrics_summary['Taxa. Entrega'] = metrics_summary['Entrega']/metrics_summary['Enviados']
                        metrics_summary['Taxa de Abertos'] = metrics_summary['Abertos']/metrics_summary['Entrega']
                        metrics_summary['Taxa Clicados'] = metrics_summary['Clicados']/metrics_summary['Entrega']
                        cursor.close()
                elif 'conversions' in q.datasource and metric == 'visits':
                    cnx=mysql.connector.connect(
                        user=config('MYSQL_DB_USER'),
                        password=config('MYSQL_DB_PASS'),
                        host=config('MYSQL_DB_HOST'),
                        database=q.db_name)
                    stmt = "SELECT  SUM({}) as {} FROM {} WHERE {} like '%{}%'".format(
                                'visits', 
                                dict(cls.METRICS)[metric],
                                '_'.join([q.company_source, q.datasource]),
                                q.data_columns.split(',')[0],
                                clorus_id
                            )
                    with cnx.cursor(buffered=True, dictionary=True) as cursor:  
                        cursor.execute(stmt)
                        row = cursor.fetchone()
                        col_name = dict(cls.METRICS)[metric]
                        cursor.close()
                    metrics_summary.update(row)
                elif 'opportunities' in q.datasource and metric == 'opportunities':
                    cnx=mysql.connector.connect(
                        user=config('MYSQL_DB_USER'),
                        password=config('MYSQL_DB_PASS'),
                        host=config('MYSQL_DB_HOST'),
                        database=q.db_name)
                    stmt = "SELECT  Count({}) as {} FROM {} WHERE {} like '%{}%'".format(
                                'uuid', 
                                dict(cls.METRICS)[metric],
                                '_'.join([q.company_source, q.datasource]),
                                q.data_columns.split(',')[0],
                                clorus_id
                            )
                    with cnx.cursor(buffered=True, dictionary=True) as cursor:  
                        cursor.execute(stmt)
                        row = cursor.fetchone()
                        col_name = dict(cls.METRICS)[metric]
                        cursor.close()
                    metrics_summary.update(row)
        else:
            for q in queries:
                # if not cnx:
                cnx=mysql.connector.connect(
                    user=config('MYSQL_DB_USER'),
                    password=config('MYSQL_DB_PASS'),
                    host=config('MYSQL_DB_HOST'),
                    database=q.db_name)
                for m in metrics:
                    for col in cls.get_db_table(cls, metric=m):
                        if m in cls.METRICS_CRM:
                            ## breakpoint()
                            if ('crm' in q.db_name) and (q.query_type=='2'):
                                stmt = "SHOW COLUMNS FROM {} LIKE '{}'".format(
                                '_'.join([q.company_source, q.datasource]),
                                col,
                            )
                            else: # tabela nao eh crm
                                continue
                            #     stmt = "SELECT SUM({}) as {} FROM {} WHERE products_id like '{}'".format(
                            #     col,
                            # dict(cls.METRICS)[m],
                            # '_'.join([q.company_source, 'deals']),
                            # )
                        else:    
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
                                if ('crm' in q.db_name) and (q.query_type=='2'):
                                    if m in ['deals']:
                                        stmt = "SELECT  COUNT({}) as {} FROM {} WHERE products_id like '{}'".format(
                                        col, 
                                        dict(cls.METRICS)[m],
                                        '_'.join([q.company_source, 'deals']),
                                        product_id
                                    )
                                    else:
                                        stmt = "SELECT  SUM({}) as {} FROM {} WHERE products_id like '{}'".format(
                                            col, 
                                            dict(cls.METRICS)[m],
                                            '_'.join([q.company_source, q.datasource]),
                                            product_id
                                        )
                                else:
                                    # breakpoint()
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
                                        if ('crm' in q.db_name) and (q.query_type=='2'):
                                            metrics_summary[col_name] = decimal.Decimal(metrics_summary[col_name])+row[col_name]
                                        else:
                                            metrics_summary[col_name] = metrics_summary[col_name]+row[col_name]
                                    else:
                                        metrics_summary.update(row)
                                    cursor.close()
                cnx.close()
        # breakpoint()
        if metric in cls.METRICS_DB_ANNOTATE:
            return cls.calc_annotate(
                    metric,
                    dict(cls.METRICS)[metric],
                    *metrics_summary.values()
                )
        return metrics_summary

