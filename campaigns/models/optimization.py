import datetime, json
from decouple import config
from itertools import islice
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import NotFound

from mysql.connector import errorcode
import mysql.connector
import decimal #for decimal field

from company.models import Company, CustomQuery
from accounts.models.apiuser import APIUser
from clorusapi.utils.common import CommonProduct
from clorusapi.utils.properties import lazy_property

from .campaign import Campaign

class Optimization(models.Model):
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

