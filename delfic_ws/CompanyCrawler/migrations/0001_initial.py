# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('RegisteredNumber', models.CharField(max_length=8, serialize=False, primary_key=True)),
                ('Name', models.CharField(max_length=500)),
                ('Turnover', models.IntegerField(default=0)),
                ('Profit', models.IntegerField(default=0)),
                ('Employees', models.IntegerField(default=0)),
                ('SIC', models.CharField(max_length=6)),
                ('AddressLine1', models.CharField(max_length=500)),
                ('AddressLine2', models.CharField(max_length=500)),
                ('AddressLine3', models.CharField(max_length=500)),
                ('AddressLine4', models.CharField(max_length=500)),
                ('AddressLine5', models.CharField(max_length=500)),
                ('Town', models.CharField(max_length=100)),
                ('County', models.CharField(max_length=50)),
                ('Postcode', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
