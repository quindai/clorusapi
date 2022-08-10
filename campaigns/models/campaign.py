from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext_lazy as _

from django.db import models

from decouple import config
from mysql.connector import errorcode
from rest_framework.exceptions import NotFound

import mysql.connector
import datetime
import decimal  # for decimal field
import json

from accounts.models.apiuser import APIUser
from clorusapi.utils.common import CommonProduct
from company.models import Company, CustomQuery
from .mainmetrics import MainMetrics


class CampaignManager(models.Manager):
    """
    Manages the Campaign objects returned.
    Adds some calculated fields to the Campaign objects array
    """
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
            return (retorno, temp_date)
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

                            # breakpoint()
 
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
                    stmt = "SELECT json_unquote(products_id) as products_id,json_unquote(products_price) as products_price FROM {} WHERE JSON_CONTAINS(products_id, '{}', '$')".format(
                        '_'.join([q.company_source, 'deals']),
                        kwargs['products'][index].id_crm
                    )
                    with cnx1.cursor(buffered=True, dictionary=True) as cursor:  
                        cursor.execute(stmt)
                        rows = cursor.fetchall()
                        cursor.close()
                    # breakpoint()
                    sum_prices = 0
                    for row in rows:
                        index = json.loads(row['products_id']).index(int(kwargs['products'][index].id_crm))
                    # tmp_products = json.loads(row['products_id'])
                        sum_prices = sum_prices + json.loads(row['products_price'])[index]


                    # stmt = "SELECT NULLIF(0,SUM(price)) as {} FROM {} WHERE products_id like '{}'".format(
                    #     'Revenue',
                    #     '_'.join([q.company_source, 'deals']),
                    #     kwargs['products'][index].id_crm
                    # )
                    
                    # TODO
                    # close_date(crm) < expiration_date(campaign)
                    # stmt_deals = "SELECT COUNT(id) as DEALS_COUNT FROM {} WHERE products_id like '{}'".format(
                    #     '_'.join([q.company_source, 'deals']),
                    #     kwargs['products'][index].id_crm
                    # )
                    # with cnx1.cursor(buffered=True, dictionary=True) as cursor:  
                    #     cursor.execute(stmt)
                    #     row = cursor.fetchone()
                    # metrics_summary['Revenue'] = decimal.Decimal(metrics_summary['Revenue'])+row['Revenue']
                    metrics_summary['Revenue'] = metrics_summary['Revenue']+sum_prices
                        # cursor.close()
                    # with cnx1.cursor(buffered=True, dictionary=True) as cursor:
                    #     cursor.execute(stmt_deals)
                    #     row = cursor.fetchone()
                    # deals = deals+row['DEALS_COUNT']
                    deals = deals+len(rows)
                        # cursor.close()
                    rows = None
                # cnx1.close()
        # breakpoint()
        spend = list(MainMetrics.calc_metric('spend', kwargs['queries'], kwargs['id_clorus']).values())[0]
        # breakpoint()
        # calc ROAS

        if spend == 0:
            metrics_summary['ROAS'] = 0
        else:
            metrics_summary['ROAS'] = (metrics_summary['Revenue'] - spend)/spend
        
        # elif m == "CAC":
        if deals == 0:
            metrics_summary['CAC'] = 0
        else:
            metrics_summary['CAC'] = spend/deals
        return json.dumps(metrics_summary, cls=DjangoJSONEncoder)

    def get_queryset_with_status(self, *args, **kwargs):
        retorno = self.filter(
            company=APIUser.objects.get(user=args[0]).active_company
            )
        if not retorno.exists():
            raise NotFound('Não existe nenhuma Campanha para a empresa ativa.')
        # tempcq = CustomQuery.objects.get(pk=retorno[0].custom_query_id)
        tempcq = retorno[0].custom_query
        
        # pega todos custom_query e busca as métricas em todos para somar
        # queries = retorno[0].custom_query.company.company_rel.filter(query_type='1') # campanhas
        # queries = retorno[0].custom_query.company.company_rel.all()
        queries = [x.custom_query for x in retorno]
        # metrics = retorno[0].custom_query.company.custommetrics_set.all()
        status, end_date = self.get_recent_date(tempcq, retorno[0].clorus_id)
        return retorno.annotate(
            metrics_summary = models.Value(
                self.get_metrics_campaign(metrics=['Leads','Revenue','ROAS','CAC'], queries=queries, campaign=retorno,products=retorno[0].campaign_details.all(), id_clorus=retorno[0].clorus_id)),
            status = models.Value(status),
            end_date = models.Value(end_date.date())
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
    #TODO
    # Funil select metric to show by id
    # [51, 1, 52,2]
    funil_ids = models.CharField(max_length=255, default='')
    clorus_id = models.CharField(max_length=100, default='')
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
    start_date = models.DateTimeField()
    last_change = models.DateTimeField(blank=True, null=True)

    objects = CampaignManager()

    class Meta:
        ordering = ['id']
