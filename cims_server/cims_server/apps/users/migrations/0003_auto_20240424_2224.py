# Generated by Django 3.2.23 on 2024-04-24 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20240424_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identitycard',
            name='valid_to',
            field=models.DateField(verbose_name='有效期终止日'),
        ),
        migrations.AlterField(
            model_name='passport',
            name='valid_to',
            field=models.DateField(verbose_name='有效期终止日'),
        ),
    ]
