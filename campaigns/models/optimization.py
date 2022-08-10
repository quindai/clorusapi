from django.db import models
from .campaign import Campaign

class Optimization(models.Model):
    """
    Campaign Optimization
    Business related logic.
    """
    DETAIL_RESULT = [
        ('1','Negativo'),
        ('2','Positivo'),
        ('3','Neutro')
    ]
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    date_created = models.DateField(db_index=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    hypothesis = models.TextField()
    result = models.TextField()
    result_type = models.CharField(max_length=2, choices=DETAIL_RESULT)

    class Meta:
        ordering = ['date_created']

