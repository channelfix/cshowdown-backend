# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-03 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0020_auto_20180328_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='bio',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
    ]
