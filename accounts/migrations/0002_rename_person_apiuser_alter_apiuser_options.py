# Generated by Django 4.0.2 on 2022-02-14 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Person',
            new_name='APIUser',
        ),
        migrations.AlterModelOptions(
            name='apiuser',
            options={'ordering': ['-name'], 'verbose_name': 'Usuário'},
        ),
    ]