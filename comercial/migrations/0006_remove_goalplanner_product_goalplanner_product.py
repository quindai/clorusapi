# Generated by Django 4.0.2 on 2022-04-08 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0005_remove_goalplanner_general_goal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goalplanner',
            name='product',
        ),
        migrations.AddField(
            model_name='goalplanner',
            name='product',
            field=models.ManyToManyField(default=1, to='comercial.Product', verbose_name='Produto'),
        ),
    ]
