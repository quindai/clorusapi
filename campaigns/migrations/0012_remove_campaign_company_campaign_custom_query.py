# Generated by Django 4.0.2 on 2022-04-27 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0019_alter_company_logo'),
        ('campaigns', '0011_campaign_clorus_id_alter_campaign_budget_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='company',
        ),
        migrations.AddField(
            model_name='campaign',
            name='custom_query',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='company.customquery'),
        ),
    ]