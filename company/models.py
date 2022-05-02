from decouple import config
from django.db import models, DatabaseError
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from mysql.connector import errorcode
import mysql.connector


class Company(models.Model):
    # selecao de funil
    DETAIL_FUNIL = [
        ('1','V'),
        ('2','Y'),
    ]

    cnpj = models.CharField(max_length=14, db_index=True)
    name = models.CharField(max_length=200, verbose_name="Nome da Empresa")
    logo = models.TextField()
    funil = models.CharField(max_length=2, choices=DETAIL_FUNIL, default='1')

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Empresa"
        ordering = ['-name']


class CustomMetrics(models.Model):
    DETAIL_METRICS = [
        ('1','Impressões'),
        ('2','Cliques'),
        ('3','Alcance'),
        ('4','Views de Vídeo/Áudio'),
        ('5','25% Views de Vídeo/Áudio'),
        ('6','50% Views de Vídeo/Áudio'),
        ('7','75% Views de Vídeo/Áudio'),
        ('8','100% Views de Vídeo/Áudio'),
        ('9','Custo'),
    ]
    DETAIL_METRICS_DB = [
        ('1',['impressions']),
        ('2',['clicks']),
        ('3',['reach']),
        ('4',['video_p25_watched_views', 'video_views']),
        ('5',['video_p25_watched_views', 'video_quartile_p25_rate', 'Twentyfive_Percent_View']),
        ('6',['video_p50_watched_views', 'video_quartile_p50_rate', 'Fifty_Percent_View']),
        ('7',['video_p75_watched_views', 'video_quartile_p75_rate', 'Seventyfive_Percent_View']),
        ('8',['video_p100_watched_views', 'video_quartile_p100_rate', 'Completed_view']),
        ('9',['spend', 'Cost']),
    ]
    DETAIL_STEP = [tuple([str(x),x]) for x in range(1,5)]

    step = models.CharField(max_length=2, choices=DETAIL_STEP, default='1', verbose_name="Etapa")
    id_name = models.CharField(max_length=2, choices=DETAIL_METRICS, verbose_name="Escolha a Métrica")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Métrica'

    def get_db_table(self, **kwargs):
        # for q in kwargs['queries']:
        #     cnx=mysql.connector.connect(
        #         user=config('MYSQL_DB_USER'),
        #         password=config('MYSQL_DB_PASS'),
        #         host=config('MYSQL_DB_HOST'),
        #         database=q.db_name)
        #     stmt = {
        #     '1': "SELECT COUNT({}) FROM {} WHERE id_clorus like '{}'".format(
        #             m.get_db_table(), 
        #             '_'.join([q.company_source, q.datasource]),
        #             kwargs['id_clorus']),
        #         }.get(self.id_name)
        
        return dict(self.DETAIL_METRICS_DB)[self.id_name][0]
    # def get_metric_value(self, rows):
    #     pass

    # def query(self):
    #     with CustomQuery.objects.get(company=self.company) as customquery:
        # try:
        #     cnx=mysql.connector.connect(
        #         user=config('MYSQL_DB_USER'),
        #         password=config('MYSQL_DB_PASS'),
        #         host=config('MYSQL_DB_HOST'),
        #         database='') 
        #     stmt = "SELECT * FROM "+ \
        #         '_'.join([customquery.company_source, customquery.datasource])
                
    #             with cnx.cursor(buffered=True, dictionary=True) as cursor:  
    #                 cursor.execute(stmt)
    #                 rows = cursor.fetchall()
    #                 cursor.close()
    #         except Exception:
    #             pass
    #         else:
    #             return self.get_metric_value(rows)
    #         finally:
    #             cnx.close()

    def __str__(self):
        return '{}'.format(dict(self.DETAIL_METRICS)[self.id_name])

class CustomQuery(models.Model):
    # tipo de query: campanha | crm
    
    _CAMPANHA = '1'
    _CRM = '2'
    _DEALS = '3'
    DETAIL_QUERY_TYPE = [
        ('1','Campanha'),
        ('2','CRM'),
        # ('3','CRM DEALS')
    ]
    def validate_db_name(value):
        try:
            cnx=mysql.connector.connect(
                user=config('MYSQL_DB_USER'),
                password=config('MYSQL_DB_PASS'),
                host=config('MYSQL_DB_HOST'),
                database=value)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise ValidationError(
                    _('%(value)s tem algo errado com a sua senha e usuário.'),
                params={'value': value},)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise ValidationError(
                    _('%(value)s schema não existe, conexão não estabelecida.'),
                params={'value': value},)
        else:
            cnx.close()

    # se for CRM não possui id_clorus
    query_type = models.CharField(max_length=2, choices=DETAIL_QUERY_TYPE, default='1')
    db_name = models.CharField(max_length=100, validators =[validate_db_name], 
                    help_text="Nome do Schema no banco MySql. Exemplo: client_data") #exemplo client_data
    company_source = models.CharField(max_length=100, 
                    help_text="Nome da empresa no banco MySQL. Exemplo: sebraeal|sebrae") #[sebraeal|sebrae]
    datasource = models.CharField(max_length=100, null=True, 
                    blank=True, help_text="Nome do social. Exemplo: googleads|facebookads|programatica") #[googleads|facebookads|programatica]
    data_columns = models.TextField(null=True, blank=True, help_text="Colunas da tabela separadas por vírgula. A primeira coluna tem que conter o idclorus. Exemplo: campaign_id, campaign_name")
    company = models.ForeignKey(Company, related_name='company_rel', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Query Personalizada"
        verbose_name_plural = "Queries Personalizadas"
        # ordering = ['datasource']
    
    def clean(self, *args, **kwargs): 
        try:
            if self.db_name:
                if self.company_source:
                    ret = self.company_source
                    if self.datasource:
                        ret = '_'.join([self.company_source,self.datasource])
                    cnx=mysql.connector.connect(
                        user=config('MYSQL_DB_USER'),
                        password=config('MYSQL_DB_PASS'),
                        host=config('MYSQL_DB_HOST'),
                        database=self.db_name)
                    cursor = cnx.cursor()
                    stmt = "SHOW TABLES LIKE '{}'".format(ret)
                    cursor.execute(stmt)
                    result = cursor.fetchall()
                    if not result :
                        raise ValidationError("Verifique Company source e Datasource. Erro ao adicionar a busca, tabela não existe.")
                    
                    # valida a query pelo tipo
                    # buscar as colunas aqui
                    stmt = {
                        self._CAMPANHA: "SHOW COLUMNS FROM {} WHERE Field IN {}".format(ret, ('campaign_id', 'Campaign ID')),
                        self._CRM: "SHOW COLUMNS FROM {} WHERE Field IN {}".format(ret, ('active', 'sku')),
                    }.get(self.query_type)

                    if len(self.data_columns.strip())>0:
                        stmt = "SHOW COLUMNS FROM {} WHERE Field IN {}".format(ret, tuple(self.data_columns.strip().split(',')))
                    
                    cursor.execute(stmt)
                    result = cursor.fetchall()
                    if not result:
                    # if ['campaign_id', 'Campaign ID'] not in result.keys():
                        raise ValidationError(f"Erro ao adicionar a busca. Precisa preenchar as colunas de '{dict(self.DETAIL_QUERY_TYPE)[self.query_type]}'.")
                    cursor.close()
        except mysql.connector.errors.ProgrammingError as error:
            raise ValidationError(error)
        else:
            cnx.close()
        super(CustomQuery, self).clean(*args, **kwargs)

    def query(self, group_by=False, group_column='id_clorus'):
        try:
            cnx=mysql.connector.connect(
                user=config('MYSQL_DB_USER'),
                password=config('MYSQL_DB_PASS'),
                host=config('MYSQL_DB_HOST'),
                database=self.db_name) 
            stmt = "SELECT * FROM "+ \
                '_'.join([self.company_source,self.datasource])
            # if len(self.data_columns)>0:
            data_columns = [t.strip() for t in tuple(self.data_columns.split(',')) if t]
            if self.data_columns:
                if group_by:
                    stmt = "SELECT {} FROM {} GROUP BY {}".format( 
                        ','.join(data_columns), 
                        '_'.join([self.company_source,self.datasource]),
                        group_column
                    )
                else:
                    stmt = "SELECT {} FROM {}".format( 
                        ','.join(data_columns), 
                        '_'.join([self.company_source,self.datasource])
                    )
            with cnx.cursor(buffered=True, dictionary=True) as cursor:  
                cursor.execute(stmt)
                rows = cursor.fetchall()
                cursor.close()
        except mysql.connector.errors.ProgrammingError as error:
            raise ValidationError(error)
        except Exception as e:
            raise DatabaseError(
                    _('Ocorreu o erro %(e)s.'),
                params={'value': e},)
        else:
            return rows
        finally:
            cnx.close()

    def __str__(self):
        return '{} {}'.format(self.company_source, self.datasource)
