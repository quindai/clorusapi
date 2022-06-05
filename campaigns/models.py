import datetime, json
from decouple import config
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from mysql.connector import errorcode
import mysql.connector

from comercial.models import Comercial
from company.models import Company, CustomQuery
from accounts.models.apiuser import APIUser
from clorusapi.utils.common import CommonProduct

from rest_framework.exceptions import NotFound
import decimal #for decimal field
from django.core.serializers.json import DjangoJSONEncoder

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
        ('roas','ROAS'),
        ('cac','CAC - Custo de Aquisição de Cliente'),
        ('budget','Verba'),
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
    ]
    # Métricas que dependem de outras métricas para serem calculadas
    METRICS_DB_ANNOTATE = [
        'ctr',
        'cpc',
        'cpv',
        'cpl',
        'roas',
        'cac',
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
        'revenue',
        'deals'
    ]

    def get_db_table(cls, **kwargs):
        return dict(cls.METRICS_DB)[kwargs['metric']]

    def calc_annotate(metric, human_metric, *args):
        # breakpoint()
        return {
            'ctr': {human_metric: args[0]/args[1]},
            'cpc': {human_metric: args[0]/args[1]},
            'cpv': {human_metric: args[0]/args[1]},
            'cpl': {human_metric: args[0]/args[1]},
            'roas': {human_metric: (args[1] - args[0])/args[0] },
            'cac': {human_metric: args[0]/args[1]},
        }.get(metric)

    def calc_catering(metric):
        return {
            'ctr': ['impressions','clicks'],
            'cpc': ['spend','clicks'],
            'cpv': ['spend','views'],
            'cpl': ['spend','leads'],
            'roas': ['spend','revenue'],
            'cac': ['spend','deals']
        }.get(metric)

    @classmethod
    def calc_metric(cls, metric, queries, clorus_id, product_id=None, cnx=None):
        # breakpoint()
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
                            stmt = "SHOW COLUMNS from {} LIKE '{}'".format(
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
        ## breakpoint()
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
        except Exception as e:
            raise ValidationError({'error':e, 'detail':f'Clorus ID {args[1]} não encontrado.'})
        else:
            return retorno
        finally:
            cnx.close()

    # def get_calc_metric(self, metric):
    #     # métricas calculadas
    #     return {
    #         #CPC - Custo por Clique: f"select sum(cost)/NULLIF(SUM(clicks), 1) as CPC from test.sebraeal_facebookads;"
    #         'Leads': "SELECT SUM({}) as Leads FROM {}",
    #         'Revenue':f"select sum(cost)/NULLIF(SUM(clicks), 1) as CPC from test.sebraeal_facebookads;",
    #         'ROAS':f"select sum(cost)/NULLIF(SUM(clicks), 1) as CPC from test.sebraeal_facebookads;",
    #         'CAC':f"select sum(cost)/NULLIF(SUM(clicks), 1) as CPC from test.sebraeal_facebookads;"
    #     }.get(metric)
        
    def get_metrics_campaign(self, **kwargs):
        metrics_summary = {
            'Leads': 0,
            'Revenue': 0,
            'ROAS': 0,
            'CAC': 0
        }
 
        for q in kwargs['queries']:
            try:
                if q.datasource == 'conversions':
                    stmt = "SHOW COLUMNS FROM {} LIKE '{}'".format(
                        '_'.join([q.company_source, q.datasource]),
                        'conversion'
                    )
                    cnx=mysql.connector.connect(
                    user=config('MYSQL_DB_USER'),
                    password=config('MYSQL_DB_PASS'),
                    host=config('MYSQL_DB_HOST'),
                    database=q.db_name)
                    with cnx.cursor(buffered=True) as cursor:  
                        cursor.execute(stmt)
                        row = cursor.fetchone()
                        cursor.close()
                    if row:
                        stmt = "SELECT CAST(SUM(conversion) as SIGNED) as {} FROM {} WHERE id_clorus LIKE '{}'".format(
                        'Leads',
                        '_'.join([q.company_source, q.datasource]),
                        kwargs['id_clorus']
                        )

                        with cnx.cursor(buffered=True, dictionary=True) as cursor:  
                            cursor.execute(stmt)
                            row = cursor.fetchone()
 
                            metrics_summary['Leads'] = metrics_summary['Leads']+row['Leads']
                    # else:
                        # metrics_summary.update(row)
                        row=None
                        cursor.close()
                        cnx.close()
            except mysql.connector.Error as err:
                cnx.close()
                if err.errno == errorcode.ER_BAD_FIELD_ERROR:
                    raise NotFound(
                    {'detail':f'{err}',
                    'cause': _(f'Tabela {".".join([q.db_name, "_".join([q.company_source, q.datasource])])} no MySQL não possui a coluna especificada.')}
                )

        # calc spend
        ptr = list(kwargs['products'].values_list('custom_query')[0])
        
        aa=CustomQuery.objects.filter(pk__in=ptr)

        # calc Revenue
        for index, q in enumerate(aa):
            if ('crm' in q.db_name) and (q.query_type=='2'):
                stmt = "SHOW COLUMNS from {} LIKE '{}'".format(
                    '_'.join([q.company_source, q.datasource]),
                    'price',
                )
                cnx1=mysql.connector.connect(
                    user=config('MYSQL_DB_USER'),
                    password=config('MYSQL_DB_PASS'),
                    host=config('MYSQL_DB_HOST'),
                    database=q.db_name)
                with cnx1.cursor(buffered=True) as cursor:  
                    cursor.execute(stmt)
                    row = cursor.fetchone()
                    cursor.close()
                if row:
                    stmt = "SELECT SUM(price) as {} FROM {} WHERE products_id like '{}'".format(
                        'Revenue',
                        '_'.join([q.company_source, 'deals']),
                        kwargs['products'][index].id_crm
                    )
                    deals = 0
                    # TODO
                    # close_date(crm) < expiration_date(campaign)
                    stmt_deals = "SELECT COUNT(id) as DEALS_COUNT FROM {} WHERE products_id like '{}'".format(
                        '_'.join([q.company_source, 'deals']),
                        kwargs['products'][index].id_crm
                    )
                    with cnx1.cursor(buffered=True, dictionary=True) as cursor:  
                        cursor.execute(stmt)
                        row = cursor.fetchone()
                        metrics_summary['Revenue'] = decimal.Decimal(metrics_summary['Revenue'])+row['Revenue']
                        cursor.close()
                    with cnx1.cursor(buffered=True, dictionary=True) as cursor:
                        cursor.execute(stmt_deals)
                        row = cursor.fetchone()
                        deals = deals+row['DEALS_COUNT']
                        cursor.close()
                    row = None
                cnx1.close()
        spend = list(MainMetrics.calc_metric('spend', kwargs['queries'], kwargs['id_clorus']).values())[0]
        # breakpoint()
        # calc ROAS
        metrics_summary['ROAS'] = (metrics_summary['Revenue'] - decimal.Decimal(spend))/decimal.Decimal(spend)
        
        # elif m == "CAC":
        metrics_summary['CAC'] = spend/deals
        return json.dumps(metrics_summary, cls=DjangoJSONEncoder)

    def get_queryset_with_status(self, *args, **kwargs):
        # breakpoint()
        retorno = self.filter(
            custom_query__company=
            APIUser.objects.get(user=args[0]).active_company
            )
        if not retorno:
            raise NotFound('Não existe nenhuma Campanha para a empresa ativa.')
        tempcq = CustomQuery.objects.get(pk=retorno[0].custom_query_id)
        
        # pega todos custom_query e busca as métricas em todos para somar
        # queries = retorno[0].custom_query.company.company_rel.filter(query_type='1') # campanhas
        queries = retorno[0].custom_query.company.company_rel.all()
        # metrics = retorno[0].custom_query.company.custommetrics_set.all()
        
        return retorno.annotate(
            # metrics_summary = models.Value(
            #     self.get_metrics_sum(metrics=metrics, queries=queries, id_clorus=retorno[0].clorus_id)),
            metrics_summary = models.Value(
                self.get_metrics_campaign(metrics=['Leads','Revenue','ROAS','CAC'], queries=queries, products=retorno[0].campaign_details.all(), id_clorus=retorno[0].clorus_id)),
            status = models.Value(self.get_recent_date(
                tempcq, retorno[0].clorus_id
            ))
        )

class CampaignMetaDetail(CommonProduct):
    """ 
    custom_query de produto, para rastreamento da origem desse item
    """
    custom_query = models.ForeignKey(CustomQuery, on_delete=models.CASCADE, verbose_name="Query de origem do item em raw_data")
    class Meta:
        verbose_name = 'Detalhes de Campanha'

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
    goal_budget = models.CharField(max_length=255, default='', verbose_name='Soma de valor monetário (Total proveniente de Meta Geral)')
    goal_quantity = models.IntegerField(default=1, verbose_name='Soma da meta dos produtos')
    campaign_details = models.ManyToManyField(CampaignMetaDetail)
    custom_query = models.ForeignKey(CustomQuery, on_delete=models.CASCADE, verbose_name="Query da campanha em raw_data")
    # comercial = models.ForeignKey(Comercial, on_delete=models.CASCADE, null=True)
    # company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    budget = models.CharField(max_length=255, default='', verbose_name="Valor Investido")
    date_created = models.DateTimeField(auto_now_add=True)
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
    date_created = models.DateField(auto_now_add=True, db_index=True)
    description = models.TextField()
    hypothesis = models.TextField()
    result = models.TextField()
    result_type = models.CharField(max_length=2, choices=DETAIL_RESULT)

    class Meta:
        ordering = ['date_created']