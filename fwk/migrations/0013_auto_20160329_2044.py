# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 18:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fwk', '0012_auto_20160329_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Der Preis dieses Auftrags inkl. Mehrwertsteuer. Wird automatisch anhand         des Tarifs und der Strecke berechnet, kann aber \xfcberschrieben werden.', max_digits=4, null=True, verbose_name='Preis'),
        ),
        migrations.AlterField(
            model_name='order',
            name='rate',
            field=models.ForeignKey(blank=True, help_text='Der Tarif wird automatisch anhand der Packst\xfccke berechnet, kann         aber \xfcberschrieben werden.', null=True, on_delete=django.db.models.deletion.CASCADE, to='fwk.Rate', verbose_name='Tarif'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('UNFINISHED', '0. unfertig'), ('NEW', '1. neu'), ('CONFIRMED', '2. best\xe4tigt'), ('PICKED_UP', '3. abgeholt'), ('DELIVERED', '4. ausgeliefert'), ('CANCELED', 'x. storniert')], default='UNFINISHED', max_length=10),
        ),
    ]