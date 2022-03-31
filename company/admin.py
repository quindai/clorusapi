from django.contrib import admin

from company.models import Company, CustomQuery, CustomMetrics

class CustomQueryInline(admin.StackedInline):
    model = CustomQuery
    extra = 1

class CustomMetricsInline(admin.StackedInline):
    model = CustomMetrics
    extra = 1

class CompanyAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Dados da Empresa', {'fields': ('cnpj','name','logo')}),
    ]
    inlines = [CustomMetricsInline, CustomQueryInline]

admin.site.register(Company, CompanyAdmin)