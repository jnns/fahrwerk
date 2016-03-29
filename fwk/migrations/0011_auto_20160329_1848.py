# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fwk', '0010_auto_20160329_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Der Preis dieses Auftrags inkl. Mehrwertsteuer. Wird automatisch anhand         des Tarifs und der Strecke berechnet, kann aber \xfcberschrieben werden.', max_digits=4, verbose_name='Preis'),
        ),
    ]
