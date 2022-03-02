from django.db import models
from company.models import CustomQuery
# Create your models here.

class Product(models.Model):
    pass

class Campaign(models.Model):
    pass
    # GOAL_SELECT = [
    #     ('1','Colocar Opções')
    # ]
    # name = models.CharField(max_length=255, verbose_name="Nome da Campanha")
    # image = models.TextField()
    # goal = models.CharField(max_length=2, choices=GOAL_SELECT, 
    #                         verbose_name="Objetivo da Campanha", help_text='')
    # goal_description = models.TextField(verbose_name="Descrição do Objetivo")
    # goal_budget = models.CharField(verbose_name='Meta (Total proveniente de Meta Geral)')
    # products =models.ForeignKey(Product, on_delete=models.CASCADE,help_text='Escolha de produtos (Caso Meta Segmentada)')
    # budget = models.CharField(verbose_name="Valor Investido")
