# Generated by Django 4.0.2 on 2022-05-23 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0021_alter_custommetrics_step'),
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='goal_quantity',
            field=models.IntegerField(default=1, verbose_name='Soma da meta dos produtos'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='custom_query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.customquery', verbose_name='Query da campanha em raw_data'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='goal_budget',
            field=models.CharField(default='', max_length=255, verbose_name='Meta monetária (Total proveniente de Meta Geral)'),
        ),
        migrations.AlterField(
            model_name='campaignmetadetail',
            name='custom_query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.customquery', verbose_name='Query de origem do item em raw_data'),
        ),
    ]
