# Generated by Django 4.0.2 on 2022-04-01 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comercial',
            name='visualization',
        ),
        migrations.AddField(
            model_name='comercial',
            name='visualization_mon',
            field=models.BooleanField(default=False, verbose_name='Visualização Monetária'),
        ),
        migrations.AddField(
            model_name='comercial',
            name='visualization_quant',
            field=models.BooleanField(default=False, verbose_name='Visualização Quantitativa'),
        ),
        migrations.AlterField(
            model_name='comercial',
            name='begin_date',
            field=models.DateField(db_index=True, verbose_name='Data de Início'),
        ),
        migrations.AlterField(
            model_name='comercial',
            name='repeat_periodicity',
            field=models.BooleanField(default=False, verbose_name='Repetir Periodicidade'),
        ),
    ]
