# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fwk', '0005_auto_20160319_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW', 'neu'), ('CONFIRMED', 'best\xe4tigt'), ('PICKED_UP', 'abgeholt'), ('DELIVERED', 'ausgeliefert'), ('CANCELED', 'storniert')], default='NEW', max_length=10),
        ),
    ]
