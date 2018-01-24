# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-07 09:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(blank=True, max_length=50, verbose_name='事件的唯一key')),
                ('event_stat', models.CharField(blank=True, max_length=50, verbose_name='状态')),
                ('event_time', models.DateTimeField(auto_now=True, verbose_name='事件状态时间')),
                ('opreater_name', models.CharField(default='actanble', max_length=10, verbose_name='操作员名字')),
                ('extra_add', models.TextField(default='', verbose_name='添加备注')),
                ('connect_person', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='状态参与人员')),
            ],
            options={
                'verbose_name': '事件详细',
            },
        ),
    ]