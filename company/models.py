from django.db import models
from decouple import config
import mysql.connector
from mysql.connector import errorcode
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    cnpj = models.CharField(max_length=14, db_index=True)
    name = models.CharField(max_length=200, verbose_name="Nome da Empresa")
    logo = models.CharField(max_length=10)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Empresa"
        ordering = ['-name']


class CustomQuery(models.Model):
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
        except mysql.connector.errors.ProgrammingError as error:
            raise ValidationError(error)
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
                row = cursor.fetchall()
                cursor.close()
        except Exception:
            pass
        else:
            return row
        finally:
            cnx.close()

    def __str__(self):
        return '{} {}'.format(self.company_source, self.datasource)
