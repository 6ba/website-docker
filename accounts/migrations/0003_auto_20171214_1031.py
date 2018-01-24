# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-14 02:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_projuser_shenfen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projuser',
            name='nickname',
        ),
        migrations.AlterField(
            model_name='projuser',
            name='mugshot',
            field=models.ImageField(default='mugshots/logo400x400.jpg', upload_to='uploads/mugshots', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='projuser',
            name='shenfen',
            field=models.CharField(default='网络管理员', max_length=50, verbose_name='身份'),
        ),
    ]