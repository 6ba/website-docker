# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-08 05:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventdetail',
            name='event',
            field=models.IntegerField(verbose_name='事件|alertuser表唯一的id'),
        ),
    ]
