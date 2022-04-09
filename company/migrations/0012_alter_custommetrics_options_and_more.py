# Generated by Django 4.0.2 on 2022-04-01 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0011_alter_custommetrics_options_company_funil_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='custommetrics',
            options={'verbose_name': 'Métrica'},
        ),
        migrations.AlterField(
            model_name='custommetrics',
            name='id_name',
            field=models.CharField(choices=[('1', 'Impressões'), ('2', 'Cliques'), ('3', 'Alcance'), ('4', 'Views de Vídeo/Áudio'), ('5', '25% Views de Vídeo/Áudio'), ('6', '50% Views de Vídeo/Áudio'), ('7', '75% Views de Vídeo/Áudio'), ('8', '100% Views de Vídeo/Áudio'), ('9', 'Custo')], max_length=2, verbose_name='Escolha a Métrica'),
        ),
        migrations.AlterField(
            model_name='custommetrics',
            name='step',
            field=models.CharField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], default='1', max_length=2, verbose_name='Etapa'),
        ),
    ]