# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=2000)),
                ('value_en', models.CharField(max_length=2000, null=True)),
                ('value_tr', models.CharField(max_length=2000, null=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name': 'Setting',
                'verbose_name_plural': 'Settings',
            },
        ),
    ]
