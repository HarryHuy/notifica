# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-15 20:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifica', '0002_activity_participate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='participate',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
