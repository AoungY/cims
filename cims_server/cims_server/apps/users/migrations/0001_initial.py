# Generated by Django 3.2.23 on 2024-04-24 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GovernmentUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.TextField(verbose_name='公钥')),
                ('private_key', models.TextField(verbose_name='私钥')),
            ],
            options={
                'verbose_name': '政府用户',
                'verbose_name_plural': '政府用户',
                'db_table': 'ms_government_user',
            },
        ),
        migrations.CreateModel(
            name='OrdinaryUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.TextField(verbose_name='公钥')),
                ('private_key', models.TextField(verbose_name='私钥')),
            ],
            options={
                'verbose_name': '普通用户',
                'verbose_name_plural': '普通用户',
                'db_table': 'ms_ordinary_user',
            },
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='姓名')),
                ('gender', models.CharField(choices=[('m', '男'), ('f', '女')], max_length=1, verbose_name='性别')),
                ('birth_date', models.DateField(verbose_name='出生年月日')),
                ('issuing_authority', models.CharField(max_length=40, verbose_name='颁发机构')),
                ('valid_from', models.DateField(auto_now_add=True, verbose_name='有效期起始日')),
                ('valid_to', models.DateField(verbose_name='有效期终止日')),
                ('photo', models.ImageField(upload_to='photos/', verbose_name='照片')),
                ('document_number', models.CharField(max_length=64, verbose_name='证件编号')),
                ('previous_document_number', models.CharField(blank=True, max_length=64, null=True, verbose_name='前证件编号')),
                ('next_document_number', models.CharField(blank=True, max_length=64, null=True, verbose_name='未来证件编号')),
                ('another_document_number', models.CharField(blank=True, max_length=64, null=True, verbose_name='创建当前证件时另一个证件的编号')),
                ('nationality', models.CharField(max_length=5, verbose_name='国籍')),
                ('passport_number', models.CharField(max_length=18, verbose_name='护照号码')),
                ('issuing_country', models.CharField(max_length=8, verbose_name='颁发国家')),
                ('ordinary_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.ordinaryuser', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '护照',
                'verbose_name_plural': '护照',
                'db_table': 'ms_passport',
            },
        ),
        migrations.CreateModel(
            name='IdentityCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='姓名')),
                ('gender', models.CharField(choices=[('m', '男'), ('f', '女')], max_length=1, verbose_name='性别')),
                ('birth_date', models.DateField(verbose_name='出生年月日')),
                ('issuing_authority', models.CharField(max_length=40, verbose_name='颁发机构')),
                ('valid_from', models.DateField(auto_now_add=True, verbose_name='有效期起始日')),
                ('valid_to', models.DateField(verbose_name='有效期终止日')),
                ('photo', models.ImageField(upload_to='photos/', verbose_name='照片')),
                ('document_number', models.CharField(max_length=64, verbose_name='证件编号')),
                ('previous_document_number', models.CharField(blank=True, max_length=64, null=True, verbose_name='前证件编号')),
                ('next_document_number', models.CharField(blank=True, max_length=64, null=True, verbose_name='未来证件编号')),
                ('another_document_number', models.CharField(blank=True, max_length=64, null=True, verbose_name='创建当前证件时另一个证件的编号')),
                ('ethnicity', models.CharField(max_length=5, verbose_name='民族')),
                ('address', models.CharField(max_length=70, verbose_name='居住地址')),
                ('id_number', models.CharField(max_length=18, verbose_name='身份证号')),
                ('ordinary_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.ordinaryuser', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '身份证',
                'verbose_name_plural': '身份证',
                'db_table': 'ms_identity_card',
            },
        ),
    ]
