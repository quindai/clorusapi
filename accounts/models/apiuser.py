from django.db import models
from .user import User
from company.models import Company

class APIUser(models.Model):
    TYPE_OF = [
        ('1','Marketeer'),
        ('2', 'Cliente')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #User._meta.get_field('username').validators[1].limit_value = 255
    # User._meta.get_field('username').verbose_name = 'Email do Usuário'
   
    # Tipo de usuário
    user_type = models.CharField(max_length=1, choices=TYPE_OF, verbose_name='Tipo do usuário.', help_text='1 - Marketeer; 2 - Cliente;',)
    
    # Nome da pessoa
    name = models.CharField(max_length=255, verbose_name='Nome da pessoa')
    active_company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    star_companies = models.ManyToManyField(Company, related_name='star_company', blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Usuário da API'
        verbose_name_plural = 'Usuários da API'
        ordering = ['-name']

