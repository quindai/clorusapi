# Generated by Django 4.0.2 on 2022-06-03 09:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0003_alter_campaign_goal_budget'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]