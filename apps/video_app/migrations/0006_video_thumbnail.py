# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-26 00:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0005_auto_20190625_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='thumbnail',
            field=models.CharField(default='null', max_length=255),
            preserve_default=False,
        ),
    ]
