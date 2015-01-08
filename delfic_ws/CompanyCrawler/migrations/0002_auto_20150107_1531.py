# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CompanyCrawler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanySiteLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('TypeKey', models.CharField(max_length=20)),
                ('Url', models.CharField(max_length=200)),
                ('Company', models.ForeignKey(to='CompanyCrawler.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='company',
            name='WebsiteUrl',
            field=models.CharField(default=None, max_length=200),
            preserve_default=True,
        ),
    ]
