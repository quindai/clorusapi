# Generated by Django 4.0.2 on 2022-02-17 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_alter_company_cnpj'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['-name'], 'verbose_name': 'Empresa'},
        ),
    ]
