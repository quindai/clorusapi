import datetime, json
from decouple import config
from itertools import islice
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
        # 'conversions'
    ]
    METRICS_MARKETEER = [
        'budget'
    ]
    METRICS_HYBRID = [
        'balance',
        'invested'
    ]

    def get_db_table(cls, **kwargs):
        return dict(cls.METRICS_DB)[kwargs['metric']]

    def calc_annotate(metric, human_metric, *args):
        breakpoint()
        # args[1] = 0 if args[1]==None else args[1]
        # args[0] = 0 if args[0]==None else args[0]
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
                'balance': {human_metric: args[0]-args[1]},
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
            queries = [] # garante que não vai executar outro trecho
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
            metrics = ['email_' + x for x in cls.calc_catering(metric)]
            for q in queries:
                if 'emails' in q.datasource:
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
                # metrics_summary[dict(cls.METRICS)[metrics[0]]], 
                # metrics_summary[dict(cls.METRICS)[metrics[1]]]
                )
        return metrics_summary

class CampaignManager(models.Manager):
    def get_recent_date(self, *args):
        # breakpoint()
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

            temp_date = datetime.datetime.strptime(row[0], '%Y-%m-%d')
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

        metrics_summary['Saldo'] = list(MainMetrics.calc_metric('balance', kwargs['queries'], kwargs['id_clorus'], campaigns=kwargs['campaign']).values())[0]
        # breakpoint()

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
        # breakpoint()
        # calc spend
        ptr = list(kwargs['products'].values_list('custom_query')[0])
        
        # breakpoint()
        aa=CustomQuery.objects.filter(pk__in=ptr)

        # calc Revenue
        deals = 0
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
        # retorno = self.filter(
        #     custom_query__company=
        #     APIUser.objects.get(user=args[0]).active_company
        #     )
        retorno = self.filter(
            company=APIUser.objects.get(user=args[0]).active_company
            )
        if not retorno:
            raise NotFound('Não existe nenhuma Campanha para a empresa ativa.')
        # tempcq = CustomQuery.objects.get(pk=retorno[0].custom_query_id)
        tempcq = retorno[0].custom_query
        
        # pega todos custom_query e busca as métricas em todos para somar
        # queries = retorno[0].custom_query.company.company_rel.filter(query_type='1') # campanhas
        # queries = retorno[0].custom_query.company.company_rel.all()
        queries = [x.custom_query for x in retorno]
        # metrics = retorno[0].custom_query.company.custommetrics_set.all()
        
        return retorno.annotate(
            # metrics_summary = models.Value(
            #     self.get_metrics_sum(metrics=metrics, queries=queries, id_clorus=retorno[0].clorus_id)),
            metrics_summary = models.Value(
                self.get_metrics_campaign(metrics=['Leads','Revenue','ROAS','CAC'], queries=queries, campaign=retorno,products=retorno[0].campaign_details.all(), id_clorus=retorno[0].clorus_id)),
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
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    budget = models.CharField(max_length=255, default='', verbose_name="Valor Investido")
    date_created = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(blank=True, null=True)

    objects = CampaignManager()

    class Meta:
        ordering = ['id']


class Criativos(models.Model):
    # TYPE_OF = [
    #     ('1','Display'),
    #     ('2','Vídeo'),
    #     ('3','Áudio'),
    #     ('4','Pesquisa'),
    #     ('5','Landing Page'),
    # ]

    GOAL_SELECT = [
        ('1','Tráfego'),
        ('2','Reconhecimento de marca'),
        ('3','Engajamento'),
        ('4','Geração de lead'),
        ('5','Vendas'),
    ]
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    ad_group_id = models.CharField(max_length=100)
    ad_id = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    tipo_midia = models.CharField(max_length=100, null=True, blank=True)
    # name = models.CharField(max_length=255)
    # criativo_type = models.CharField(max_length=2,choices=TYPE_OF)
    # goal = models.CharField(max_length=2, default='', choices=GOAL_SELECT, 
                            # verbose_name="Objetivo da Campanha", help_text='')
    goal = models.CharField(max_length=100, null=True, blank=True)
    channel = models.CharField(max_length=100, null=True, blank=True)
    format = models.CharField(max_length=100, null=True, blank=True)
    #metrics
    ## alcance, ctr, cliques, cpc, cpl, leads, investimento

def save_criativos(instance):
    clorus_id = instance.clorus_id
    query = instance.custom_query
    cnx=mysql.connector.connect(
        user=config('MYSQL_DB_USER'),
        password=config('MYSQL_DB_PASS'),
        host=config('MYSQL_DB_HOST'),
        database=query.db_name)

    stmt = "SELECT * FROM {} WHERE Campaign LIKE '%{}%' GROUP BY `Ad ID`".format(
        '_'.join([query.company_source, query.datasource]),
        clorus_id,
    )

    with cnx.cursor(buffered=True, dictionary=True) as cursor:  
        cursor.execute(stmt)
        rows = cursor.fetchall()
        cursor.close()
    cnx.close()

    criativos = (Criativos(
        ad_group_id= row['Ad group ID'],
        ad_id= row['Ad ID'],
        description= row['Description'],
        tipo_midia= row['tipo_midia'],
        channel= row['channel'],
        format= row['format'],
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

