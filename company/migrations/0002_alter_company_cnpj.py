# Generated by Django 4.0.2 on 2022-02-16 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='cnpj',
            field=models.CharField(db_index=True, max_length=11),
        ),
    ]
