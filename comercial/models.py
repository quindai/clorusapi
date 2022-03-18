from turtle import update
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime

class ComercialManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        # super().get_queryset().filter(repeat_periodicity=True).update(

        # )
        retorno= super().get_queryset(*args, **kwargs).annotate(
                #if repeat_periodicity == True
                #if begin_date== expiration_date
                #   begin_date=expiration_date
                #   expiration_date=begin_date+period_days
                #   
                # period_days = (models.Case(
                #     models.When(periodicity=Comercial._WEEKLY, then=models.Value(7)),
                #     models.When(periodicity=Comercial._MONTHLY, then=models.Value(30)),
                #     models.When(periodicity=Comercial._SEMESTERLY, then=models.Value(180)),
                #     models.When(periodicity=Comercial._YEARLY, then=models.Value(360)),
                #     default=models.Value(0),
                #     output_field=models.IntegerField(),
                # )),
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
                ))
                ,
                status = models.ExpressionWrapper(
                    #When(F(repeat_periodicty=True),then)
                    models.Q(expiration_date__gt=models.functions.Now()),
                    # models.Q(expiration_date__gt=models.F('_begin_date')),
                    output_field=models.BooleanField()
                )
            )
        retorno.filter(models.Q(repeat_periodicity=True) & models.Q(expiration_date__lte=models.functions.Now())
            ).update(_begin_date = models.F('expiration_date'))
        return retorno
            # .annotate(
            #         expiration_date= models.ExpressionWrapper(
            #         models.F('_begin_date') + datetime.timedelta(days=1)*models.F('period_days'),
            #         output_field=models.DateField(db_index=True)
            #     # models.Case(
            #     #     models.When(models.Q(repeat_periodicity=True) & models.Q(expiration_date__gt=models.F('begin_date')), 
            #     #     then=(models.F('begin_date') + models.F('period_days')), output_field=models.DateField(db_index=True))
            #     )
            # )
        # else:
            # return super().get_queryset()

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
                    verbose_name="Visualização")
    begin_date = models.DateField(db_index=True)
    _begin_date = models.DateField(db_index=True, null=True, blank=True)
    # expiration_date = models.DateField(db_index=True)
    periodicity = models.CharField(max_length=1, choices=DETAIL_PERIODICITY, 
                    verbose_name="Seleção de Periodicidade")
    repeat_periodicity = models.BooleanField(default=False)
    segmentation = models.CharField(max_length=2, choices=DETAIL_SEGMENTATION,
                    verbose_name="Segmentação")

    objects = ComercialManager()

@receiver(post_save, sender=Comercial)
def pre_save_handler(sender, **kwargs):
#     """after saving Comercial, change _begin_date"""
    # breakpoint()
    instance = kwargs.get('instance')
    Comercial.objects.filter(pk=instance.pk).update(_begin_date = instance.begin_date)
    
