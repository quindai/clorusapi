from django.contrib import admin

from company.models import Company, CustomQuery

class CustomQueryInline(admin.TabularInline):
    model = CustomQuery
    extra = 1

class CompanyAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Dados da Empresa', {'fields': ('cnpj','name','logo')}),
    ]
    inlines = [CustomQueryInline]

admin.site.register(Company, CompanyAdmin)