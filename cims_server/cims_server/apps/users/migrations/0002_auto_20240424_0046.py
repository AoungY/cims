# Generated by Django 3.2.23 on 2024-04-24 00:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrdinaryUser',
            new_name='IdentityCard',
        ),
        migrations.RenameModel(
            old_name='GovernmentUser',
            new_name='Passport',
        ),
        migrations.AlterModelOptions(
            name='identitycard',
            options={'verbose_name': '身份证', 'verbose_name_plural': '身份证'},
        ),
        migrations.AlterModelOptions(
            name='passport',
            options={'verbose_name': '护照', 'verbose_name_plural': '护照'},
        ),
        migrations.AlterModelTable(
            name='identitycard',
            table='ms_identity_card',
        ),
        migrations.AlterModelTable(
            name='passport',
            table='ms_passport',
        ),
    ]
