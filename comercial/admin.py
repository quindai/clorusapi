from django.contrib import admin
from .models import Comercial, Product, GoalPlanner
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.

admin.site.register(Comercial, SimpleHistoryAdmin)
admin.site.register(Product, SimpleHistoryAdmin)
admin.site.register(GoalPlanner, SimpleHistoryAdmin)