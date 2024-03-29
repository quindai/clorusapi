# Generated by Django 4.0.2 on 2022-06-19 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0008_alter_criativos_channel_alter_criativos_format_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='criativos',
            options={'ordering': ['id']},
        ),
        migrations.RenameField(
            model_name='criativos',
            old_name='goal',
            new_name='objective',
        ),
        migrations.AddField(
            model_name='criativos',
            name='click_goal',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='criativos',
            name='cpc_goal',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='criativos',
            name='cpl_goal',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='criativos',
            name='ctr_goal',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='criativos',
            name='invested_goal',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='criativos',
            name='leads_goal',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='criativos',
            name='range_goal',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
