from django.db import models
from company.models import CustomQuery
# Create your models here.

class Product(models.Model):
    # unidade
    # meta
    pass

class Campaign(models.Model):
    pass
    GOAL_SELECT = [
        ('1','Tráfego'),
        ('2','Reconhecimento de marca'),
        ('3','Engajamento'),
        ('4','Geração de lead'),
        ('5','Vendas'),
    ]
    name = models.CharField(max_length=255, default='1', verbose_name="Nome da Campanha")
    # image = models.TextField(default='1')
    goal = models.CharField(max_length=2, default=1, choices=GOAL_SELECT, 
                            verbose_name="Objetivo da Campanha", help_text='')
    goal_description = models.TextField(default='1', verbose_name="Descrição do Objetivo")
    goal_budget = models.CharField(max_length=255, default='1', verbose_name='Meta (Total proveniente de Meta Geral)')
    # products =models.ForeignKey(Product, on_delete=models.CASCADE, help_text='Escolha de produtos (Caso Meta Segmentada)')
    budget = models.CharField(max_length=255, default='1', verbose_name="Valor Investido")
