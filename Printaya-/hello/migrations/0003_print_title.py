# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 06:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20170213_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='print',
            name='title',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
    ]