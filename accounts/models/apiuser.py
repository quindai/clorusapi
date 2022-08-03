from django.db import models
from .user import User
from company.models import Company

"""
APIUser has relation One to One with ./user.User
"""
class APIUser(models.Model):
    TYPE_OF = [
        ('1','Marketeer'),
        ('2', 'Cliente')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
   
    # Tipo de usuário
    user_type = models.CharField(max_length=1, choices=TYPE_OF, verbose_name='Tipo do usuário.', help_text='1 - Marketeer; 2 - Cliente;',)
    
    # Nome da pessoa
    name = models.CharField(max_length=255, verbose_name='Nome da pessoa')
    active_company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    star_companies = models.ManyToManyField(Company, related_name='star_company', blank=True)
    telephone = models.CharField(max_length=16, verbose_name="Telefone", default='')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Usuário da API'
        verbose_name_plural = 'Usuários da API'
        ordering = ['-name']

