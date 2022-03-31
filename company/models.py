from tabnanny import verbose
from django.db import models
from decouple import config
import mysql.connector
from mysql.connector import errorcode
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    # selecao de funil
    cnpj = models.CharField(max_length=14, db_index=True)
    name = models.CharField(max_length=200, verbose_name="Nome da Empresa")
    logo = models.CharField(max_length=10)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Empresa"
        ordering = ['-name']

class CustomMetrics(models.Model):
    DETAIL_METRICS = [
        (1,'Impressões'),
        (2,'Cliques'),
        (3,'Alcance'),
        (4,'Views de Vídeo/Áudio'),
        (5,'25% Views de Vídeo/Áudio'),
        (6,'50% Views de Vídeo/Áudio'),
        (7,'75% Views de Vídeo/Áudio'),
        (8,'100% Views de Vídeo/Áudio'),
        (9,'Custo'),
    ]

    id_name = models.IntegerField(max_length=2, choices=DETAIL_METRICS)
    # company = models.ForeignKey(Company, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Métrica'

    def get_metric_value(self, rows):
        pass

    def query(self):
        with CustomQuery.objects.get(company=self.company) as customquery:
            try:
                cnx=mysql.connector.connect(
                    user=config('MYSQL_DB_USER'),
                    password=config('MYSQL_DB_PASS'),
                    host=config('MYSQL_DB_HOST'),
                    database=customquery.db_name) 
                stmt = "SELECT * FROM "+ \
                    '_'.join([customquery.company_source, customquery.datasource])
                    
                with cnx.cursor(buffered=True, dictionary=True) as cursor:  
                    cursor.execute(stmt)
                    rows = cursor.fetchall()
                    cursor.close()
            except Exception:
                pass
            else:
                return self.get_metric_value(rows)
            finally:
                cnx.close()

    def __str__(self):
        return '{}'.format(self.DETAIL_METRICS[self.id_name][1])

class CustomQuery(models.Model):
    # adiciona somente queries que possuem a coluna campaign_id
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

    db_name = models.CharField(max_length=100, validators =[validate_db_name], 
                    help_text="Nome do Schema no banco MySql. Exemplo: client_data") #exemplo client_data
    company_source = models.CharField(max_length=100, 
                    help_text="Nome da empresa no banco MySQL. Exemplo: sebraeal|sebrae") #[sebraeal|sebrae]
    datasource = models.CharField(max_length=100, null=True, 
                    blank=True, help_text="Nome do social. Exemplo: googleads|facebookads|programatica") #[googleads|facebookads|programatica]
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
                    
                    # verifica se possui a coluna campaign_id
                    stmt = "SHOW COLUMNS FROM {} WHERE Field IN {}".format(ret, ('campaign_id', 'Campaign ID'))
                    cursor.execute(stmt)
                    result = cursor.fetchall()
                    if not result:
                    # if ['campaign_id', 'Campaign ID'] not in result.keys():
                        raise ValidationError("Erro ao adicionar a busca. Tabela do MySQL não contém 'Campaign ID'.")
                    cursor.close()
        except mysql.connector.errors.ProgrammingError as error:
            raise ValidationError(error)
        else:
            cnx.close()
        super(CustomQuery, self).clean(*args, **kwargs)

    def query(self):
        try:
            cnx=mysql.connector.connect(
                user=config('MYSQL_DB_USER'),
                password=config('MYSQL_DB_PASS'),
                host=config('MYSQL_DB_HOST'),
                database=self.db_name) 
            stmt = "SELECT * FROM "+ \
                '_'.join([self.company_source,self.datasource])
                 
            with cnx.cursor(buffered=True, dictionary=True) as cursor:  
                cursor.execute(stmt)
                rows = cursor.fetchall()
                cursor.close()
        except Exception:
            pass
        else:
            return rows
        finally:
            cnx.close()

    def __str__(self):
        return '{} {}'.format(self.company_source, self.datasource)
