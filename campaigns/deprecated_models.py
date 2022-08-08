# import datetime, json
# from decouple import config
# from itertools import islice
# from django.db import models
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from django.utils import timezone
# from django.core.serializers.json import DjangoJSONEncoder

# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

# from rest_framework.exceptions import NotFound

# from mysql.connector import errorcode
# import mysql.connector
# import decimal #for decimal field

# from company.models import Company, CustomQuery
# from accounts.models.apiuser import APIUser
# from clorusapi.utils.common import CommonProduct
# from clorusapi.utils.properties import lazy_property


# TODO 
# SELECT SUM(impressions), id_clorus FROM test.sebraeal_programatica where id_clorus='#238470';

# class MainMetrics():
#     """
#     This class returns the value of metrics.
#     Guarantees that only mapped metrics are returned.
#     """
#     METRICS = [ # Nome de todas as métricas
#         ('impressions','Impressões'),
#         ('clicks','Cliques'),
#         ('range','Alcance'),
#         ('views','Views de Vídeo/Áudio'),
#         ('views_25','25% Views de Vídeo/Áudio'),
#         ('views_50','50% Views de Vídeo/Áudio'),
#         ('views_75','75% Views de Vídeo/Áudio'),
#         ('views_100','100% Views de Vídeo/Áudio'),
#         ('ctr','CTR - Taxa de Cliques'),
#         ('cpv','CPV - Custo por View'),
#         ('cpc','CPC - Custo por Clique'),
#         ('cpl','CPL - Custo por lead'),
#         ('visits','Visitas'),
#         ('deals','Vendas'),
#         ('revenue','Receita'),
#         ('spend','Custo (Spend ou Investido)'),
#         ('leads','Leads'),
#         # ('invested','Investimento / Investido'),
#         ('roas','ROAS'),
#         ('cac','CAC - Custo de Aquisição de Cliente'),
#         ('budget','Verba'),
#         ('balance','Saldo'),
#         ('invested','Investido'),
#         ('conversions','Conversão'),
#     ]
#     METRICS_DB = [ # métricas de soma
#         ('impressions',['impressions']),
#         ('clicks',['clicks']),
#         ('range',['reach']),
#         ('views',['video_p25_watched_views', 'video_views']),
#         ('views_25',['video_p25_watched_views', 'video_quartile_p25_rate', 'Twentyfive_Percent_View']),
#         ('views_50',['video_p50_watched_views', 'video_quartile_p50_rate', 'Fifty_Percent_View']),
#         ('views_75',['video_p75_watched_views', 'video_quartile_p75_rate', 'Seventyfive_Percent_View']),
#         ('views_100',['video_p100_watched_views', 'video_quartile_p100_rate', 'Completed_view']),
#         ('spend',['spend', 'Cost']),
#         ('leads',['conversion']),
#         ('deals',['id']),
#         ('revenue',['price']),
#         ('conversions', ['conversion'])
#     ]
#     # Métricas que dependem de outras métricas para serem calculadas
#     METRICS_DB_ANNOTATE = [
#         'ctr',
#         'cpc',
#         'cpv',
#         'cpl',
#         'roas',
#         'cac',
#         'balance',
#         'invested',
#         # 'visits',
#     ]
#     METRICS_API_KEY = [
#         'impressions',
#         'clicks',
#         'range',
#         'views_25',
#         'views_50',
#         'views_75',
#         'views_100',
#         'spend',
#         'leads',
#         'conversions',
#     ]
#     METRICS_CRM = [
#         'revenue',
#         'deals'
#     ]
#     METRICS_RD = [
#         'email',
#         'opportunities',
#         'visits',
#         # 'conversions'
#     ]
#     METRICS_MARKETEER = [
#         'budget'
#     ]
#     METRICS_HYBRID = [
#         'balance',
#         # 'invested'
#     ]

#     def get_db_table(cls, **kwargs):
#         return dict(cls.METRICS_DB)[kwargs['metric']]

#     def calc_annotate(metric, human_metric, *args):
#         if args[1] == 0:
#             return {human_metric: args[1]}
#         try:
#             return {
#                 'ctr': {human_metric: args[0]/args[1]},
#                 'cpc': {human_metric: args[0]/args[1]},
#                 'cpv': {human_metric: args[0] if args[1]==0 else args[0]/args[1]},
#                 'cpl': {human_metric: args[0]/args[1]},
#                 'roas': {human_metric: (args[1] - args[0])/args[0] },
#                 'cac': {human_metric: args[0]/args[1]},
#                 'balance': {human_metric: 0 if args[0]-args[1] < 0 else args[0]-args[1]},
#                 'invested': {human_metric: sum(args)}
#             }.get(metric)
#         except Exception as e:
#             raise ValidationError({'error':e, 'detail':f'Métrica {human_metric} com divisor zero 0, não pode ser calculada.'})

#     def calc_catering(metric):
#         return {
#             'ctr': ['impressions','clicks'],
#             'cpc': ['spend','clicks'],
#             'cpv': ['spend','views'],
#             'cpl': ['spend','leads'],
#             'roas': ['spend','revenue'],
#             'cac': ['spend','deals'],
#             'balance': ['budget','spend'],
#             #TODO
#             # retificar invested
#             'invested': ['spend','cpc','cpv','cac','cpl'],
#             'email': ['sent', 'delivered', 'opened', 'tx_opened', 'tx_clicks']
#         }.get(metric)

#     @classmethod
#     def calc_metric(cls, metric, queries, clorus_id, product_id=None, campaigns=None, cnx=None):
#         # breakpoint()
#         if not 'metrics_summary' in vars():
#             metrics_summary = {}
#         if metric in cls.METRICS_DB_ANNOTATE:
#             metrics = cls.calc_catering(metric)
#         elif metric in cls.METRICS_MARKETEER:
#             metrics_summary = {dict(cls.METRICS)[metric]: campaigns.aggregate(models.Sum('budget'))['budget__sum']}
#             queries = [] # garante que não vai executar outro trecho
#         elif metric not in [*cls.METRICS_API_KEY, *cls.METRICS_RD, 'all']:
#             raise NotFound(
#                 _(f'{metric} métrica não existe, ou não foi mapeada.')
#             )
#         else:
#             metrics = cls.METRICS_API_KEY if metric=='all' else [metric]
#         # breakpoint()
#         if metric in cls.METRICS_HYBRID:
#             for m in metrics:
#                 if dict(cls.METRICS)[m] in metrics_summary.keys():
#                     metrics_summary[dict(cls.METRICS)[m]] = metrics_summary[dict(cls.METRICS)[m]] + metrics_summary.update(
#                         cls.calc_metric(m, queries, clorus_id, product_id, campaigns, cnx)
#                     )[dict(cls.METRICS)[m]]
#                 else:
#                     metrics_summary.update(
#                         cls.calc_metric(m, queries, clorus_id, product_id, campaigns, cnx)
#                     )
#         elif metric in cls.METRICS_RD:
#             # breakpoint()
#             for q in queries:
#                 if 'emails' in q.datasource and metric == 'email':
#                     metrics = ['email_' + x for x in cls.calc_catering(metric)]
#                     cnx=mysql.connector.connect(
#                         user=config('MYSQL_DB_USER'),
#                         password=config('MYSQL_DB_PASS'),
#                         host=config('MYSQL_DB_HOST'),
#                         database=q.db_name)
#                     # stmt = "SELECT SUM({}) FROM {} WHERE {} LIKE '%{}%'"
#                     stmt = """SELECT SUM(`{}`) as {}, 
#                                 SUM(`{}`) as {}, 
#                                 SUM(`{}`) as {}, 
#                                 SUM(`{}`) as {} 
#                                 FROM {}""".format(
#                         'Leads selecionados',
#                         'Enviados',
#                         'Entregues',
#                         'Entrega',
#                         'Aberturas (unicas)',
#                         'Abertos',
#                         'Cliques (unicos)',
#                         'Clicados',
#                         '_'.join([q.company_source, q.datasource]),
#                     )

#                     with cnx.cursor(buffered=True, dictionary=True) as cursor:  
#                         cursor.execute(stmt)
#                         row = cursor.fetchone()
#                         # col_name = dict(cls.METRICS)[m]
#                         col_name = ['Enviados','Entrega','Abertos','Clicados']
#                         if set(col_name).issubset(metrics_summary.keys()):
#                                 metrics_summary[col_name[0]] = metrics_summary[col_name[0]]+row[col_name[0]]
#                                 metrics_summary[col_name[1]] = metrics_summary[col_name[1]]+row[col_name[1]]
#                                 metrics_summary[col_name[2]] = metrics_summary[col_name[2]]+row[col_name[2]]
#                                 metrics_summary[col_name[3]] = metrics_summary[col_name[3]]+row[col_name[3]]
#                         else:
#                             metrics_summary.update(row)
#                         metrics_summary['Taxa. Entrega'] = metrics_summary['Entrega']/metrics_summary['Enviados']
#                         metrics_summary['Taxa de Abertos'] = metrics_summary['Abertos']/metrics_summary['Entrega']
#                         metrics_summary['Taxa Clicados'] = metrics_summary['Clicados']/metrics_summary['Entrega']
#                         cursor.close()
#                 elif 'conversions' in q.datasource and metric == 'visits':
#                     cnx=mysql.connector.connect(
#                         user=config('MYSQL_DB_USER'),
#                         password=config('MYSQL_DB_PASS'),
#                         host=config('MYSQL_DB_HOST'),
#                         database=q.db_name)
#                     stmt = "SELECT  SUM({}) as {} FROM {} WHERE {} like '%{}%'".format(
#                                 'visits', 
#                                 dict(cls.METRICS)[metric],
#                                 '_'.join([q.company_source, q.datasource]),
#                                 q.data_columns.split(',')[0],
#                                 clorus_id
#                             )
#                     with cnx.cursor(buffered=True, dictionary=True) as cursor:  
#                         cursor.execute(stmt)
#                         row = cursor.fetchone()
#                         col_name = dict(cls.METRICS)[metric]
#                         cursor.close()
#                     metrics_summary.update(row)
#                 elif 'opportunities' in q.datasource and metric == 'opportunities':
#                     cnx=mysql.connector.connect(
#                         user=config('MYSQL_DB_USER'),
#                         password=config('MYSQL_DB_PASS'),
#                         host=config('MYSQL_DB_HOST'),
#                         database=q.db_name)
#                     stmt = "SELECT  Count({}) as {} FROM {} WHERE {} like '%{}%'".format(
#                                 'uuid', 
#                                 dict(cls.METRICS)[metric],
#                                 '_'.join([q.company_source, q.datasource]),
#                                 q.data_columns.split(',')[0],
#                                 clorus_id
#                             )
#                     with cnx.cursor(buffered=True, dictionary=True) as cursor:  
#                         cursor.execute(stmt)
#                         row = cursor.fetchone()
#                         col_name = dict(cls.METRICS)[metric]
#                         cursor.close()
#                     metrics_summary.update(row)
#         else:
#             for q in queries:
#                 # if not cnx:
#                 cnx=mysql.connector.connect(
#                     user=config('MYSQL_DB_USER'),
#                     password=config('MYSQL_DB_PASS'),
#                     host=config('MYSQL_DB_HOST'),
#                     database=q.db_name)
#                 for m in metrics:
#                     for col in cls.get_db_table(cls, metric=m):
#                         if m in cls.METRICS_CRM:
#                             ## breakpoint()
#                             if ('crm' in q.db_name) and (q.query_type=='2'):
#                                 stmt = "SHOW COLUMNS FROM {} LIKE '{}'".format(
#                                 '_'.join([q.company_source, q.datasource]),
#                                 col,
#                             )
#                             else: # tabela nao eh crm
#                                 continue
#                             #     stmt = "SELECT SUM({}) as {} FROM {} WHERE products_id like '{}'".format(
#                             #     col,
#                             # dict(cls.METRICS)[m],
#                             # '_'.join([q.company_source, 'deals']),
#                             # )
#                         else:    
#                             stmt = "SHOW COLUMNS FROM {} LIKE '{}'".format(
#                                 '_'.join([q.company_source, q.datasource]),
#                                 col
#                             )
#                         # if column exists
#                         with cnx.cursor(buffered=True) as cursor:  
#                             cursor.execute(stmt)
#                             row = cursor.fetchone()
#                             cursor.close()
#                             if row:
#                                 if ('crm' in q.db_name) and (q.query_type=='2'):
#                                     if m in ['deals']:
#                                         stmt = "SELECT  COUNT({}) as {} FROM {} WHERE products_id like '{}'".format(
#                                         col, 
#                                         dict(cls.METRICS)[m],
#                                         '_'.join([q.company_source, 'deals']),
#                                         product_id
#                                     )
#                                     else:
#                                         stmt = "SELECT  SUM({}) as {} FROM {} WHERE products_id like '{}'".format(
#                                             col, 
#                                             dict(cls.METRICS)[m],
#                                             '_'.join([q.company_source, q.datasource]),
#                                             product_id
#                                         )
#                                 else:
#                                     # breakpoint()
#                                     stmt = "SELECT  CAST(SUM({}) AS SIGNED) as '{}' FROM {} WHERE id_clorus like '{}'".format(
#                                         col, 
#                                         dict(cls.METRICS)[m],
#                                         '_'.join([q.company_source, q.datasource]),
#                                         clorus_id
#                                     )
#                                 with cnx.cursor(buffered=True, dictionary=True) as cursor:  
#                                     cursor.execute(stmt)
#                                     row = cursor.fetchone()
#                                     col_name = dict(cls.METRICS)[m]
#                                     if col_name in metrics_summary.keys():
#                                         if ('crm' in q.db_name) and (q.query_type=='2'):
#                                             metrics_summary[col_name] = decimal.Decimal(metrics_summary[col_name])+row[col_name]
#                                         else:
#                                             metrics_summary[col_name] = metrics_summary[col_name]+row[col_name]
#                                     else:
#                                         metrics_summary.update(row)
#                                     cursor.close()
#                 cnx.close()
#         # breakpoint()
#         if metric in cls.METRICS_DB_ANNOTATE:
#             return cls.calc_annotate(
#                     metric,
#                     dict(cls.METRICS)[metric],
#                     *metrics_summary.values()
#                 )
#         return metrics_summary


# class CampaignManager(models.Manager):
#     def get_recent_date(self, *args):
#         # breakpoint()
#         try:
#             cnx=mysql.connector.connect(
#                 user=config('MYSQL_DB_USER'),
#                 password=config('MYSQL_DB_PASS'),
#                 host=config('MYSQL_DB_HOST'),
#                 database=args[0].db_name) 
#             stmt = "SELECT MAX(date) as date FROM {} WHERE id_clorus like '{}' HAVING MAX(date)".format(
#                 '_'.join([args[0].company_source, args[0].datasource]),
#                 args[1])
        
#         #TODO company datasource fields [rule]
#         # 1- id_clorus
#         # 2- 
#             with cnx.cursor(buffered=True) as cursor:  
#                 cursor.execute(stmt)
#                 row = cursor.fetchone()
#                 cursor.close()

#             temp_date = datetime.datetime.strptime(row[0], '%Y-%m-%d')
#             if temp_date <= datetime.datetime.now()-datetime.timedelta(days=30):
#                 retorno = 'Inativa'
#             elif temp_date < datetime.datetime.now()-datetime.timedelta(days=15):
#                 retorno = 'Pausada'
#             else: retorno = 'Ativa'
#         except mysql.connector.errors.ProgrammingError as error:
#             raise ValidationError(error)
#         except Exception as e:
#             raise ValidationError({'error':e, 'detail':f'Clorus ID {args[1]} não encontrado.'})
#         else:
#             return (retorno, temp_date)
#         finally:
#             cnx.close()

#     # def get_calc_metric(self, metric):
#     #     # métricas calculadas
#     #     return {
#     #         #CPC - Custo por Clique: f"select sum(cost)/NULLIF(SUM(clicks), 1) as CPC from test.sebraeal_facebookads;"
#     #         'Leads': "SELECT SUM({}) as Leads FROM {}",
#     #         'Revenue':f"select sum(cost)/NULLIF(SUM(clicks), 1) as CPC from test.sebraeal_facebookads;",
#     #         'ROAS':f"select sum(cost)/NULLIF(SUM(clicks), 1) as CPC from test.sebraeal_facebookads;",
#     #         'CAC':f"select sum(cost)/NULLIF(SUM(clicks), 1) as CPC from test.sebraeal_facebookads;"
#     #     }.get(metric)
        
#     def get_metrics_campaign(self, **kwargs):
#         metrics_summary = {
#             'Leads': 0,
#             'Revenue': 0,
#             'ROAS': 0,
#             'CAC': 0
#         }

#         metrics_summary['Saldo'] = list(MainMetrics.calc_metric('balance', kwargs['queries'], kwargs['id_clorus'], campaigns=kwargs['campaign']).values())[0]
#         # breakpoint()

#         for q in kwargs['queries']:
#             try:
#                 if q.datasource == 'conversions':
#                     stmt = "SHOW COLUMNS FROM {} LIKE '{}'".format(
#                         '_'.join([q.company_source, q.datasource]),
#                         'conversion'
#                     )
#                     cnx=mysql.connector.connect(
#                     user=config('MYSQL_DB_USER'),
#                     password=config('MYSQL_DB_PASS'),
#                     host=config('MYSQL_DB_HOST'),
#                     database=q.db_name)
#                     with cnx.cursor(buffered=True) as cursor:  
#                         cursor.execute(stmt)
#                         row = cursor.fetchone()
#                         cursor.close()
#                     if row:
#                         stmt = "SELECT CAST(SUM(conversion) as SIGNED) as {} FROM {} WHERE id_clorus LIKE '{}'".format(
#                         'Leads',
#                         '_'.join([q.company_source, q.datasource]),
#                         kwargs['id_clorus']
#                         )

#                         with cnx.cursor(buffered=True, dictionary=True) as cursor:  
#                             cursor.execute(stmt)
#                             row = cursor.fetchone()

#                             # breakpoint()
 
#                             metrics_summary['Leads'] = metrics_summary['Leads']+row['Leads']
#                     # else:
#                         # metrics_summary.update(row)
#                         row=None
#                         cursor.close()
#                         cnx.close()
#             except mysql.connector.Error as err:
#                 cnx.close()
#                 if err.errno == errorcode.ER_BAD_FIELD_ERROR:
#                     raise NotFound(
#                     {'detail':f'{err}',
#                     'cause': _(f'Tabela {".".join([q.db_name, "_".join([q.company_source, q.datasource])])} no MySQL não possui a coluna especificada.')}
#                 )
#         # breakpoint()
#         # calc spend
#         ptr = list(kwargs['products'].values_list('custom_query')[0])
        
#         # breakpoint()
#         aa=CustomQuery.objects.filter(pk__in=ptr)

#         # calc Revenue
#         deals = 0
#         for index, q in enumerate(aa):
#             if ('crm' in q.db_name) and (q.query_type=='2'):
#                 stmt = "SHOW COLUMNS from {} LIKE '{}'".format(
#                     '_'.join([q.company_source, q.datasource]),
#                     'price',
#                 )
#                 cnx1=mysql.connector.connect(
#                     user=config('MYSQL_DB_USER'),
#                     password=config('MYSQL_DB_PASS'),
#                     host=config('MYSQL_DB_HOST'),
#                     database=q.db_name)
#                 with cnx1.cursor(buffered=True) as cursor:  
#                     cursor.execute(stmt)
#                     row = cursor.fetchone()
#                     cursor.close()
#                 if row:
#                     stmt = "SELECT json_unquote(products_id) as products_id,json_unquote(products_price) as products_price FROM {} WHERE JSON_CONTAINS(products_id, '{}', '$')".format(
#                         '_'.join([q.company_source, 'deals']),
#                         kwargs['products'][index].id_crm
#                     )
#                     with cnx1.cursor(buffered=True, dictionary=True) as cursor:  
#                         cursor.execute(stmt)
#                         rows = cursor.fetchall()
#                         cursor.close()
#                     # breakpoint()
#                     sum_prices = 0
#                     for row in rows:
#                         index = json.loads(row['products_id']).index(int(kwargs['products'][index].id_crm))
#                     # tmp_products = json.loads(row['products_id'])
#                         sum_prices = sum_prices + json.loads(row['products_price'])[index]


#                     # stmt = "SELECT NULLIF(0,SUM(price)) as {} FROM {} WHERE products_id like '{}'".format(
#                     #     'Revenue',
#                     #     '_'.join([q.company_source, 'deals']),
#                     #     kwargs['products'][index].id_crm
#                     # )
                    
#                     # TODO
#                     # close_date(crm) < expiration_date(campaign)
#                     # stmt_deals = "SELECT COUNT(id) as DEALS_COUNT FROM {} WHERE products_id like '{}'".format(
#                     #     '_'.join([q.company_source, 'deals']),
#                     #     kwargs['products'][index].id_crm
#                     # )
#                     # with cnx1.cursor(buffered=True, dictionary=True) as cursor:  
#                     #     cursor.execute(stmt)
#                     #     row = cursor.fetchone()
#                     # metrics_summary['Revenue'] = decimal.Decimal(metrics_summary['Revenue'])+row['Revenue']
#                     metrics_summary['Revenue'] = metrics_summary['Revenue']+sum_prices
#                         # cursor.close()
#                     # with cnx1.cursor(buffered=True, dictionary=True) as cursor:
#                     #     cursor.execute(stmt_deals)
#                     #     row = cursor.fetchone()
#                     # deals = deals+row['DEALS_COUNT']
#                     deals = deals+len(rows)
#                         # cursor.close()
#                     rows = None
#                 # cnx1.close()
#         # breakpoint()
#         spend = list(MainMetrics.calc_metric('spend', kwargs['queries'], kwargs['id_clorus']).values())[0]
#         # breakpoint()
#         # calc ROAS

#         if spend == 0:
#             metrics_summary['ROAS'] = 0
#         else:
#             metrics_summary['ROAS'] = (metrics_summary['Revenue'] - spend)/spend
        
#         # elif m == "CAC":
#         if deals == 0:
#             metrics_summary['CAC'] = 0
#         else:
#             metrics_summary['CAC'] = spend/deals
#         return json.dumps(metrics_summary, cls=DjangoJSONEncoder)

#     def get_queryset_with_status(self, *args, **kwargs):
#         retorno = self.filter(
#             company=APIUser.objects.get(user=args[0]).active_company
#             )
#         if not retorno.exists():
#             raise NotFound('Não existe nenhuma Campanha para a empresa ativa.')
#         # tempcq = CustomQuery.objects.get(pk=retorno[0].custom_query_id)
#         tempcq = retorno[0].custom_query
        
#         # pega todos custom_query e busca as métricas em todos para somar
#         # queries = retorno[0].custom_query.company.company_rel.filter(query_type='1') # campanhas
#         # queries = retorno[0].custom_query.company.company_rel.all()
#         queries = [x.custom_query for x in retorno]
#         # metrics = retorno[0].custom_query.company.custommetrics_set.all()
#         status, end_date = self.get_recent_date(tempcq, retorno[0].clorus_id)
#         return retorno.annotate(
#             metrics_summary = models.Value(
#                 self.get_metrics_campaign(metrics=['Leads','Revenue','ROAS','CAC'], queries=queries, campaign=retorno,products=retorno[0].campaign_details.all(), id_clorus=retorno[0].clorus_id)),
#             status = models.Value(status),
#             end_date = models.Value(end_date.date())
#         )

    
# class CampaignMetaDetail(CommonProduct):
#     """ 
#     custom_query de produto, para rastreamento da origem desse item
#     """
#     custom_query = models.ForeignKey(CustomQuery, on_delete=models.CASCADE, verbose_name="Query de origem do item em raw_data")
#     class Meta:
#         verbose_name = 'Detalhes de Campanha'

# class Campaign(models.Model):
#     GOAL_SELECT = [
#         ('1','Tráfego'),
#         ('2','Reconhecimento de marca'),
#         ('3','Engajamento'),
#         ('4','Geração de lead'),
#         ('5','Vendas'),
#     ]
#     #TODO
#     # Funil select metric to show by id
#     # [51, 1, 52,2]
#     funil_ids = models.CharField(max_length=255, default='')
#     clorus_id = models.CharField(max_length=100, default='')
#     name = models.CharField(max_length=255, default='', verbose_name="Nome da Campanha")
#     image = models.TextField(default='')
#     goal = models.CharField(max_length=2, default='', choices=GOAL_SELECT, 
#                             verbose_name="Objetivo da Campanha", help_text='')
#     goal_description = models.TextField(default='', verbose_name="Descrição do Objetivo")
#     goal_budget = models.CharField(max_length=255, default='', verbose_name='Soma de valor monetário (Total proveniente de Meta Geral)')
#     goal_quantity = models.IntegerField(default=1, verbose_name='Soma da meta dos produtos')
#     campaign_details = models.ManyToManyField(CampaignMetaDetail)
#     custom_query = models.ForeignKey(CustomQuery, on_delete=models.CASCADE, verbose_name="Query da campanha em raw_data")
#     # comercial = models.ForeignKey(Comercial, on_delete=models.CASCADE, null=True)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
#     budget = models.CharField(max_length=255, default='', verbose_name="Valor Investido")
#     start_date = models.DateTimeField()
#     last_change = models.DateTimeField(blank=True, null=True)

#     objects = CampaignManager()

#     class Meta:
#         ordering = ['id']


# class CriativoManager(models.Manager):
#     pass
        

#     # def get_queryset(self, *args, **kwargs):
#     #     breakpoint()
#     #     return super().get_queryset(*args, **kwargs).annotate(
            
#     #     )

# class Criativos(models.Model):
#     GOAL_SELECT = [
#         ('1','Tráfego'),
#         ('2','Reconhecimento de marca'),
#         ('3','Engajamento'),
#         ('4','Geração de lead'),
#         ('5','Vendas'),
#     ]
#     campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE) 
#     ad_group_id = models.CharField(max_length=100, null=True, blank=True)  
#     ad_id = models.CharField(max_length=100, null=True, blank=True)    
#     description = models.CharField(max_length=255, null=True, blank=True)
#     tipo_midia = models.CharField(max_length=100, null=True, blank=True)    #read_only
    
#     objective = models.CharField(max_length=100, null=True, blank=True)
#     channel = models.CharField(max_length=100, null=True, blank=True)   #read_only
#     format = models.CharField(max_length=100, null=True, blank=True)    #read_only
#     range_goal = models.IntegerField(null=True, blank=True)
#     ctr_goal = models.FloatField(null=True, blank=True) #read_only
#     click_goal = models.IntegerField(null=True, blank=True) #read_only
#     cpc_goal = models.FloatField(null=True, blank=True) #read_only
#     cpl_goal = models.FloatField(null=True, blank=True) #read_only
#     cpv_goal = models.FloatField(null=True, blank=True) #read_only
#     view_goal = models.FloatField(null=True, blank=True) #read_only
#     leads_goal = models.FloatField(null=True, blank=True)
#     invested_goal = models.FloatField(null=True, blank=True) # spend
#     #metrics
#     ## alcance, ctr, cliques, cpc, cpl, leads, investimento

#     # objects = CriativoManager()

#     def calcm(self, stmt, metric, cnx):
#         with cnx.cursor(buffered=True, dictionary=True) as cursor:  
#                 cursor.execute(stmt)
#                 row = cursor.fetchone()
#                 cursor.close()
#         return row
        
#     @property
#     def get_mm(self):
#         # breakpoint()
#         campaign = Campaign.objects.filter(pk=self.campaign.pk)
#         metrics=['range','ctr','clicks','cpc','cpl','leads','invested']
#         metrics_summary = {dict(MainMetrics.METRICS)[x]:None for x in metrics}
#         if campaign.exists():
#             q = campaign[0].custom_query
#             cnx=mysql.connector.connect(
#                 user=config('MYSQL_DB_USER'),
#                 password=config('MYSQL_DB_PASS'),
#                 host=config('MYSQL_DB_HOST'),
#                 database=q.db_name)
#             stmt = """SELECT CAST(SUM(Clicks) as SIGNED) as {} 
#                 FROM {} 
#                 WHERE Campaign LIKE '%{}%' AND `Ad ID`={}
#                 """.format(
#                     dict(MainMetrics.METRICS)['clicks'],
#                     '_'.join([q.company_source, 'googleads']),
#                     campaign[0].clorus_id,
#                     self.ad_id
#                 )
#             col_name = dict(MainMetrics.METRICS)['clicks']
#             metrics_summary[col_name] = self.calcm(stmt, 'clicks', cnx).get(col_name,None)

#             stmt = """SELECT CAST(NULLIF(SUM(reach),0) as SIGNED) as {} 
#                 FROM {} 
#                 WHERE campaign_name LIKE '%{}%' AND `ad_id`={}
#                 """.format(
#                     dict(MainMetrics.METRICS)['clicks'],
#                     '_'.join([q.company_source, 'facebookads']),
#                     campaign[0].clorus_id,
#                     self.ad_id
#                 )
#             col_name = dict(MainMetrics.METRICS)['range']
#             metrics_summary[col_name] = self.calcm(stmt, 'range', cnx).get(col_name, None)
#             cnx.close()
#             return json.dumps(metrics_summary)
#         return json.dumps({'metrics':[]})

#     class Meta:
#         ordering = ['id']

# def save_criativos(instance):
#     clorus_id = instance.clorus_id
#     query = instance.custom_query
#     cnx=mysql.connector.connect(
#         user=config('MYSQL_DB_USER'),
#         password=config('MYSQL_DB_PASS'),
#         host=config('MYSQL_DB_HOST'),
#         database=query.db_name)

#     # remove espaço em branco de todos os itens separados por vírgula
#     data_columns = [t.strip() for t in tuple(query.data_columns.split(',')) if t]

#     # TODO colocar os criativos de todas as tabelas
#     stmt = "SELECT * FROM {} WHERE {} LIKE '%{}%' GROUP BY `{}`".format(
#         '_'.join([query.company_source, query.datasource]),
#         data_columns[0],
#         clorus_id,
#         data_columns[1],
#     )

#     with cnx.cursor(buffered=True, dictionary=True) as cursor:  
#         cursor.execute(stmt)
#         rows = cursor.fetchall()
#         cursor.close()
#     cnx.close()

#     criativos = (Criativos(
#         ad_group_id= row.get('Ad group ID',''),
#         ad_id= row[data_columns[1].replace('`','')],
#         description= row.get('Description',''),
#         tipo_midia= row['tipo_midia'],
#         channel= row['channel'],
#         format= row['format'],
#         objective= row.get('objective',''), 
#         campaign= instance
#     ) for row in rows)

#     batch_size = 100
#     while True:
#         batch = list(islice(criativos, batch_size))
#         if not batch:
#             break
#         Criativos.objects.bulk_create(batch, batch_size)
 

# @receiver(post_save, sender=Campaign)
# def pre_save_handler(sender, **kwargs):
# #     """after saving Campaign, update last_change"""
#     instance = kwargs.get('instance')
#     Campaign.objects.filter(pk=instance.pk).update(last_change = timezone.now())
#     save_criativos(instance)

# class Optimization(models.Model):
#     DETAIL_RESULT = [
#         ('1','Negativo'),
#         ('2','Positivo'),
#         ('3','Neutro')
#     ]
#     campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
#     date_created = models.DateField(db_index=True)
#     title = models.CharField(max_length=50)
#     description = models.TextField()
#     hypothesis = models.TextField()
#     result = models.TextField()
#     result_type = models.CharField(max_length=2, choices=DETAIL_RESULT)

#     class Meta:
#         ordering = ['date_created']

