from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Person(models.Model):
    TYPE_OF = [
        ('1','Marketeer'),
        ('2', 'Cliente')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #User._meta.get_field('username').validators[1].limit_value = 255
    # Tipo de usuário
    user_type = models.CharField(max_length=1, choices=TYPE_OF, verbose_name='Tipo do usuário.', help_text='1 - Marketeer; 2 - Cliente;',)