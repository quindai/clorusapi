# Generated by Django 4.0.2 on 2022-04-19 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0008_alter_product_id_crm'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goalplanner',
            options={'ordering': ['id'], 'verbose_name': 'Meta'},
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(verbose_name='Quantidade'),
        ),
    ]