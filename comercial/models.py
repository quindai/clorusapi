from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime
import decimal #for decimal field

class Product(models.Model):
    id_crm = models.IntegerField()
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Produto'

#3 pegar dados com model Company
class GoalPlanner(models.Model):
    general_goal = models.IntegerField()
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Meta'

    
class ComercialManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        retorno= super().get_queryset(*args, **kwargs).annotate(
                expiration_date = (models.Case(
                    models.When(periodicity=Comercial._WEEKLY, 
                        then=models.F('_begin_date') + datetime.timedelta(days=7)),
                    models.When(periodicity=Comercial._MONTHLY, 
                        then=models.F('_begin_date') + datetime.timedelta(days=30)),
                    models.When(periodicity=Comercial._SEMESTERLY, 
                        then=models.F('_begin_date') + datetime.timedelta(days=180)),
                    models.When(periodicity=Comercial._YEARLY, 
                        then=models.F('_begin_date') + datetime.timedelta(days=360)),
                    output_field=models.DateField()
                )),
                status = models.ExpressionWrapper(
                    models.Q(expiration_date__gt=models.functions.Now()),
                    output_field=models.BooleanField()
                )
            )
        retorno.filter(models.Q(repeat_periodicity=True) & models.Q(expiration_date__lte=models.functions.Now())
            ).update(_begin_date = models.F('expiration_date'))
        return retorno

class Comercial(models.Model):
    _WEEKLY='1'
    _MONTHLY='2'
    _SEMESTERLY='3'
    _YEARLY='4'
    DETAIL_PERIODICITY = [
        ('1','Semanal'),
        ('2','Mensal'),
        ('3','Semestral'),
        ('4','Anual')
    ]
    DETAIL_VISUALIZATION = [
        ('1', 'Quantitativa'),
        ('2', 'Monetária')
    ]
    DETAIL_SEGMENTATION = [
        ('1', 'Segmentada'),
        ('2', 'Não Segmentada')
    ]

    visualization = models.CharField(max_length=2, choices=DETAIL_VISUALIZATION,
                    verbose_name="Visualização", default='1')
    begin_date = models.DateField(db_index=True)
    _begin_date = models.DateField(db_index=True, null=True, blank=True)
    periodicity = models.CharField(max_length=1, choices=DETAIL_PERIODICITY, 
                    verbose_name="Seleção de Periodicidade")
    repeat_periodicity = models.BooleanField(default=False)
    segmentation = models.CharField(max_length=2, choices=DETAIL_SEGMENTATION,
                    verbose_name="Segmentação", default='1')    
    goal = models.ForeignKey(GoalPlanner, on_delete=models.CASCADE)

    objects = ComercialManager()

    #moskit
    # meta em quantidade para cada produto
    # visualization podem ser as duas opcoes
    # produto pegar valor atual dos produtos
    # todo cliente tem CRM
@receiver(post_save, sender=Comercial)
def pre_save_handler(sender, **kwargs):
#     """after saving Comercial, change _begin_date"""
    instance = kwargs.get('instance')
    Comercial.objects.filter(pk=instance.pk).update(_begin_date = instance.begin_date)
    
