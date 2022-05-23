from django.db import models

class CommonProduct(models.Model):
    id_crm = models.CharField(max_length=50)
    name = models.CharField(max_length=255, verbose_name="Nome do Produto")
    quantity = models.IntegerField(verbose_name="Quantidade")
    price = models.DecimalField(decimal_places=2, max_digits=8)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        verbose_name = 'Produto'
        ordering = ['id_crm']

class CommonComercial(models.Model):
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
    DETAIL_SEGMENTATION = [
        ('1', 'Segmentada'),
        ('2', 'Não Segmentada')
    ]
    DETAIL_VISUALIZATION = [
        ('1', 'Quantitativa'),
        ('2', 'Monetária')
    ]

    # visualization = models.CharField(max_length=2, choices=DETAIL_VISUALIZATION,
    #                 verbose_name="Visualização", default='1')
    visualization_quant = models.BooleanField(default=True, verbose_name="Visualização Quantitativa")
    visualization_mon = models.BooleanField(default=False, verbose_name="Visualização Monetária")
    begin_date = models.DateField(db_index=True, verbose_name="Data de Início")
    _begin_date = models.DateField(db_index=True, null=True, blank=True)
    periodicity = models.CharField(max_length=1, choices=DETAIL_PERIODICITY, 
                    verbose_name="Seleção de Periodicidade")
    repeat_periodicity = models.BooleanField(default=False, verbose_name="Repetir Periodicidade")
    segmentation = models.CharField(max_length=2, choices=DETAIL_SEGMENTATION,
                    verbose_name="Segmentação", default='1')    

    class Meta:
        ordering = ['id']
        abstract = True