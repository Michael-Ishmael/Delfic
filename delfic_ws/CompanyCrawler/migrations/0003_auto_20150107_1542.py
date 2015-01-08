# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CompanyCrawler', '0002_auto_20150107_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='WebsiteUrl',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
