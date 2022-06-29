# Generated by Django 4.0.2 on 2022-06-20 19:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0010_remove_campaign_date_created_campaign_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]