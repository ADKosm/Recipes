# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-11 14:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rcps', '0002_equipment_alternatives'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientalternative',
            name='original_ingredient',
        ),
    ]