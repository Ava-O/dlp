# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-10 16:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaires', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='number',
        ),
    ]
