# Generated by Django 4.0.2 on 2022-05-13 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0009_alter_goalplanner_options_alter_product_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComercialHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visualization_quant', models.BooleanField(verbose_name='Visualização Quantitativa')),
                ('visualization_mon', models.BooleanField(verbose_name='Visualização Monetária')),
                ('begin_date', models.DateField(db_index=True, verbose_name='Data de Início')),
                ('periodicity', models.CharField(max_length=255, verbose_name='Seleção de Periodicidade')),
                ('repeat_periodicity', models.BooleanField(verbose_name='Repetir Periodicidade')),
                ('segmentation', models.CharField(choices=[('1', 'Segmentada'), ('2', 'Não Segmentada')], default='1', max_length=2, verbose_name='Segmentação')),
                ('expiration_date', models.DateField()),
                ('status', models.BooleanField()),
                ('user', models.CharField(max_length=255)),
                ('modified_date', models.DateTimeField(auto_now_add=True)),
                ('comercial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comercial.comercial')),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comercial.goalplanner', verbose_name='Meta')),
            ],
        ),
    ]
