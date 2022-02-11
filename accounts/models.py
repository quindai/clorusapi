from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# from django.contrib.auth import get_user_model
# from django.contrib.auth.backends import ModelBackend

# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         UserModel = get_user_model()
#         try:
#             user = UserModel.objects.get(email=username)
#         except UserModel.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None

class Person(models.Model):
    TYPE_OF = [
        ('1','Marketeer'),
        ('2', 'Cliente')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #User._meta.get_field('username').validators[1].limit_value = 255
    User._meta.get_field('username').verbose_name = 'Email do Usuário'
   
    # Tipo de usuário
    user_type = models.CharField(max_length=1, choices=TYPE_OF, verbose_name='Tipo do usuário.', help_text='1 - Marketeer; 2 - Cliente;',)
    
    # Nome da pessoa
    name = models.CharField(max_length=255, verbose_name='Nome da pessoa')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Pessoa'
        ordering = ['-name']