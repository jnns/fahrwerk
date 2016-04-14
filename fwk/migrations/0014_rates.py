# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 19:32
from __future__ import unicode_literals

from django.db import migrations
from django.core.management import call_command


def load_rates(apps, schema_editor):
    call_command("loaddata", "fwk/migrations/rates.json")


class Migration(migrations.Migration):

    dependencies = [
        ('fwk', '0013_auto_20160329_2044'),
    ]

    operations = [
        migrations.RunPython(load_rates)
    ]