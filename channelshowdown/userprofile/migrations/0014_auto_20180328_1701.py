# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-28 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0013_auto_20180328_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='user_video',
            field=models.FileField(default=None, null=True, upload_to='profile_video/'),
        ),
    ]
