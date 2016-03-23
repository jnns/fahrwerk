# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 09:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fwk', '0004_auto_20160319_0202'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ecourier_id',
            field=models.PositiveIntegerField(blank=True, help_text='Sobald diese Tour in eCourier \xfcbernommen wurde, sollte hier die \t\tentsprechende Tournummer hinterlegt sein.', null=True, verbose_name='Tournummer'),
        ),
        migrations.AlterField(
            model_name='order',
            name='timeframe_dropoff',
            field=models.TimeField(choices=[(datetime.time(8, 0), ' 8:00 \u2013  9:00'), (datetime.time(9, 0), ' 9:00 \u2013 10:00'), (datetime.time(10, 0), '10:00 \u2013 11:00'), (datetime.time(11, 0), '11:00 \u2013 12:00'), (datetime.time(12, 0), '12:00 \u2013 13:00'), (datetime.time(13, 0), '13:00 \u2013 14:00'), (datetime.time(14, 0), '14:00 \u2013 15:00'), (datetime.time(15, 0), '15:00 \u2013 16:00'), (datetime.time(16, 0), '16:00 \u2013 17:00'), (datetime.time(17, 0), '17:00 \u2013 18:00'), (datetime.time(18, 0), '18:00 \u2013 19:00')], verbose_name='Zeitfenster Auslieferung'),
        ),
        migrations.AlterField(
            model_name='order',
            name='timeframe_pickup',
            field=models.TimeField(choices=[(datetime.time(8, 0), ' 8:00 \u2013  9:00'), (datetime.time(9, 0), ' 9:00 \u2013 10:00'), (datetime.time(10, 0), '10:00 \u2013 11:00'), (datetime.time(11, 0), '11:00 \u2013 12:00'), (datetime.time(12, 0), '12:00 \u2013 13:00'), (datetime.time(13, 0), '13:00 \u2013 14:00'), (datetime.time(14, 0), '14:00 \u2013 15:00'), (datetime.time(15, 0), '15:00 \u2013 16:00'), (datetime.time(16, 0), '16:00 \u2013 17:00'), (datetime.time(17, 0), '17:00 \u2013 18:00'), (datetime.time(18, 0), '18:00 \u2013 19:00')], verbose_name='Zeitfenster Abholung'),
        ),
    ]
