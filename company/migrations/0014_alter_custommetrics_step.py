# Generated by Django 4.0.2 on 2022-04-01 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0013_alter_custommetrics_step'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custommetrics',
            name='step',
            field=models.CharField(choices=[('1', '1'), ('2', '2')], default='1', max_length=2, verbose_name='Etapa'),
        ),
    ]
