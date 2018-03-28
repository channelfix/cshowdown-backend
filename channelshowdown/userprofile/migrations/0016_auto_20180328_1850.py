# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-28 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0015_auto_20180328_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='profile_pic',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='profile_image/'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='video_thumbnail',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='video_thumbnail/'),
        ),
    ]
