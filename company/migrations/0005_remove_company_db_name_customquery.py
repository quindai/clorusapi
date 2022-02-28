# Generated by Django 4.0.2 on 2022-02-27 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_alter_company_cnpj'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='db_name',
        ),
        migrations.CreateModel(
            name='CustomQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_name', models.CharField(blank=True, help_text='Nome do Schema no banco MySql. Exemplo: client_data', max_length=100)),
                ('company_source', models.CharField(blank=True, help_text='Nome da empresa no banco MySQL. Exemplo: sebraeal|sebrae', max_length=100)),
                ('datasource', models.CharField(blank=True, help_text='Nome do social. Exemplo: googleads|facebookads|programatica', max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_rel', to='company.company')),
            ],
            options={
                'verbose_name': 'Query Personalizada',
                'ordering': ['-db_name'],
            },
        ),
    ]
