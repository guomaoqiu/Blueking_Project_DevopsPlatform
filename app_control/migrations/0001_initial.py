# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Function_controller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('func_code', models.CharField(unique=True, max_length=64, verbose_name='\u529f\u80fdcode')),
                ('func_name', models.CharField(max_length=64, verbose_name='\u529f\u80fd\u540d\u79f0')),
                ('enabled', models.BooleanField(default=False, help_text='\u63a7\u5236\u529f\u80fd\u662f\u5426\u5bf9\u5916\u5f00\u653e\uff0c\u82e5\u9009\u62e9\uff0c\u5219\u8be5\u529f\u80fd\u5c06\u5bf9\u5916\u5f00\u653e', verbose_name='\u662f\u5426\u5f00\u542f\u8be5\u529f\u80fd')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('func_developer', models.TextField(help_text='\u591a\u4e2a\u5f00\u53d1\u8005\u4ee5\u5206\u53f7\u5206\u9694', null=True, verbose_name='\u529f\u80fd\u5f00\u53d1\u8005', blank=True)),
            ],
            options={
                'verbose_name': '\u529f\u80fd\u63a7\u5236\u5668',
                'verbose_name_plural': '\u529f\u80fd\u63a7\u5236\u5668',
            },
        ),
    ]
