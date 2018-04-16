# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiMg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_name', models.CharField(max_length=30)),
                ('api_user', models.CharField(max_length=30)),
                ('api_paas', models.CharField(max_length=80)),
                ('api_token', models.CharField(max_length=80, null=True)),
                ('token_createt', models.IntegerField(null=True)),
                ('api_url', models.CharField(unique=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='AppPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeployLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deploy_target', models.CharField(max_length=30)),
                ('deploy_app', models.CharField(max_length=30)),
                ('deploy_time', models.DateTimeField(auto_now_add=True)),
                ('deploy_user', models.CharField(max_length=30)),
                ('deploy_jid', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Hostinfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(unique=True, max_length=30, verbose_name='\u4e3b\u673a\u540d')),
                ('public_ip', models.CharField(max_length=30, verbose_name='\u516c\u7f51IP')),
                ('private_ip', models.CharField(max_length=30, verbose_name='\u5185\u7f51IP')),
                ('mem_total', models.CharField(max_length=30, verbose_name='\u603b\u5185\u5b58')),
                ('cpu_type', models.CharField(max_length=120, verbose_name='CPU\u7c7b\u578b')),
                ('num_cpus', models.CharField(max_length=30, verbose_name='CPU\u9897\u6570')),
                ('os_release', models.CharField(max_length=30, verbose_name='\u7cfb\u7edf\u7248\u672c')),
                ('kernelrelease', models.CharField(max_length=120, verbose_name='\u5185\u6838\u7248\u672c')),
            ],
        ),
        migrations.CreateModel(
            name='MatTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mattask_name', models.CharField(max_length=30)),
                ('mattask_user', models.CharField(max_length=30)),
                ('mattask_jid', models.CharField(max_length=30)),
                ('mattask_creattime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RuncmdLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('runcmd_target', models.CharField(max_length=30)),
                ('runcmd_cmd', models.CharField(max_length=30)),
                ('runcmd_time', models.DateTimeField(auto_now_add=True)),
                ('runcmd_user', models.CharField(max_length=30)),
                ('runcmd_result', models.TextField(max_length=10000000)),
            ],
        ),
        migrations.CreateModel(
            name='SaltKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key_name', models.CharField(unique=True, max_length=30)),
                ('key_status', models.CharField(max_length=30)),
            ],
        ),
    ]
