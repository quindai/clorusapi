# Generated by Django 4.0.2 on 2022-04-01 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0003_alter_comercial_visualization_quant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goalplanner',
            name='products',
        ),
        migrations.AddField(
            model_name='goalplanner',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='comercial.product', verbose_name='Produto'),
        ),
        migrations.AlterField(
            model_name='comercial',
            name='goal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comercial.goalplanner', verbose_name='Meta'),
        ),
        migrations.AlterField(
            model_name='goalplanner',
            name='general_goal',
            field=models.IntegerField(verbose_name='Meta'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome do Produto'),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name='Quantidade'),
        ),
    ]
