# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2020-05-04 10:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_app', '0008_course_is_premium'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
