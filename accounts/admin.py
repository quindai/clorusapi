from django.contrib import admin
from .models import Person
from django.contrib.auth.models import Group

admin.site.unregister(Group)
admin.site.register(Person)
