# Generated by Django 4.0.2 on 2022-06-06 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0022_company_created_at'),
        ('comercial', '0013_comercial_company_historicalcomercial_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comercial',
            name='company',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, to='company.company'),
            preserve_default=False,
        ),
    ]