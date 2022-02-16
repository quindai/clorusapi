from importlib.abc import ExecutionLoader
from django.contrib import admin
from .models import APIUser, User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.unregister(Group)
admin.site.register(APIUser)
class UserAdmin(BaseUserAdmin):
    model=User
    list_display = ('email','username')
    add_fieldsets = (
        ('Personal Info', {'fields': ('email','username','password1','password2')}),
        # ('Security', {'fields':('is_active','is_staff','is_superuser')}),
    ) 
    readonly_fields = ('date_joined',)

admin.site.register(User, UserAdmin)