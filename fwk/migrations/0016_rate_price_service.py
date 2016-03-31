# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-31 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fwk', '0015_order_directions_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='price_service',
            field=models.DecimalField(decimal_places=2, default=1.8, max_digits=4, verbose_name='Servicezeit 5 Min'),
            preserve_default=False,
        ),
    ]
