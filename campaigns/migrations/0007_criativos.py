# Generated by Django 4.0.2 on 2022-06-10 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0006_campaign_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Criativos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_group_id', models.CharField(max_length=100)),
                ('ad_id', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('tipo_midia', models.CharField(blank=True, max_length=100, null=True)),
                ('goal', models.CharField(choices=[('1', 'Tráfego'), ('2', 'Reconhecimento de marca'), ('3', 'Engajamento'), ('4', 'Geração de lead'), ('5', 'Vendas')], default='', max_length=2, verbose_name='Objetivo da Campanha')),
                ('channel', models.CharField(max_length=100)),
                ('format', models.CharField(max_length=100)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigns.campaign')),
            ],
        ),
    ]
