# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-26 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0007_auto_20180326_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='bio',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]