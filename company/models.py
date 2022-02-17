from django.db import models
# Create your models here.

class Company(models.Model):
    cnpj = models.CharField(max_length=11, db_index=True)
    name = models.CharField(max_length=200, verbose_name="Nome da Empresa")
    logo = models.CharField(max_length=10)
    db_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Empresa"
        ordering = ['-name']