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

class CampaignManager(models.Manager):
    def get_recent_date(self, *args):
        # tempcqq = CustomQuery.objects.get(pk=args[0])
        try:
            cnx=mysql.connector.connect(
                user=config('MYSQL_DB_USER'),
                password=config('MYSQL_DB_PASS'),
                host=config('MYSQL_DB_HOST'),
                database=args[0].db_name) 
            stmt = "SELECT MAX(day) as day FROM {} WHERE id_clorus like '{}' HAVING MAX(day)".format(
                '_'.join([args[0].company_source, args[0].datasource]),
                args[1])
        
            with cnx.cursor(buffered=True) as cursor:  
                cursor.execute(stmt)
                row = cursor.fetchone()
                cursor.close()

            # breakpoint()
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

    def meu_teste(self, *args, **kwargs):
        retorno =self.filter(
            custom_query__company=
            APIUser.objects.get(user=args[1]).active_company
            )
            # .annotate(
            #     cquery = models.F('custom_query'),
            #     cid = models.F('clorus_id')
            # )
        # breakpoint()
        tempcq = CustomQuery.objects.get(pk=retorno[0].custom_query_id)
        # CustomQuery.objects.get(pk=retorno[0])
        return retorno.annotate(
            status = models.Value(self.get_recent_date(
                tempcq, retorno[0].clorus_id
            ))
        )


    # def get_queryset(self, *args, **kwargs):
    #     try:
    #         breakpoint()
    #         cnx=mysql.connector.connect(
    #             user=config('MYSQL_DB_USER'),
    #             password=config('MYSQL_DB_PASS'),
    #             host=config('MYSQL_DB_HOST'),
    #             database=self.custom_query.db_name) 
    #         stmt = "SELECT MAX(day) as day FROM {} WHERE id_clorus like '{}' HAVING MAX(day)".format(
    #             '_'.join([self.custom_query.company_source, self.custom_query.datasource]),
    #             self.clorus_id
    #         )
    #         # stmt = "SELECT * FROM "+ \
    #         #     '_'.join([self.company_source,self.datasource])

    #         with cnx.cursor(buffered=True, dictionary=True) as cursor:  
    #             cursor.execute(stmt)
    #             rows = cursor.fetchall()
    #             cursor.close()

    #     except mysql.connector.errors.ProgrammingError as error:
    #         raise ValidationError(error)
    #     except (AttributeError, UnboundLocalError):
    #         return super().get_queryset(*args, **kwargs)
    #     except Exception as e:
    #         return super().get_queryset(*args, **kwargs)
    #         # raise ValidationError(
    #         #         _('Ocorreu o erro %(e)s.'),
    #         #     params={'value': e},)
    #     else:
    #         cnx.close()
    #         return super().get_queryset(*args, **kwargs).annotate(
    #             # status = {
                    
    #             # }.get(rows)
    #             status = (models.Case(
    #                 models.When(last_change__lte=models.functions.Now()-datetime.timedelta(days=30),
    #                 then=models.Value('Inativa')),
    #                 models.When(last_change__lt=models.functions.Now()-datetime.timedelta(days=15),
    #                 then=models.Value('Pausada')),
    #                 models.When(last_change__gte=models.functions.Now()-datetime.timedelta(days=15),
    #                 then=models.Value('Ativa')),
    #                 output_field=models.CharField(max_length=50)
    #             ))
    #         )
    #     # finally:


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
    # company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
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