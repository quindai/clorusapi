# Generated by Django 4.0.2 on 2022-03-02 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_alter_customquery_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customquery',
            name='datasource',
            field=models.CharField(blank=True, help_text='Nome do social. Exemplo: googleads|facebookads|programatica', max_length=100, null=True),
        ),
    ]
