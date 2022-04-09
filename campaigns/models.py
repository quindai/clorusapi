from django.db import models
from comercial.models import Comercial
# Create your models here.

class Campaign(models.Model):
    GOAL_SELECT = [
        ('1','Tráfego'),
        ('2','Reconhecimento de marca'),
        ('3','Engajamento'),
        ('4','Geração de lead'),
        ('5','Vendas'),
    ]
    name = models.CharField(max_length=255, default='', verbose_name="Nome da Campanha")
    image = models.TextField(default='1')
    goal = models.CharField(max_length=2, default=1, choices=GOAL_SELECT, 
                            verbose_name="Objetivo da Campanha", help_text='')
    goal_description = models.TextField(default='', verbose_name="Descrição do Objetivo")
    goal_budget = models.CharField(max_length=255, default='1', verbose_name='Meta (Total proveniente de Meta Geral)')
    comercial = models.ForeignKey(Comercial, on_delete=models.CASCADE, default=1)
    budget = models.CharField(max_length=255, default='1', verbose_name="Valor Investido")

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