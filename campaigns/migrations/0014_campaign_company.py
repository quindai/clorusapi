# Generated by Django 4.0.2 on 2022-04-28 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0019_alter_company_logo'),
        ('campaigns', '0013_alter_campaign_custom_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='company.company'),
        ),
    ]