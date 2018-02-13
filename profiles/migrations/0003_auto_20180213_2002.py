# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20180213_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='aciklama_en',
            field=models.CharField(max_length=50, unique=True, null=True, verbose_name='A\xe7\u0131klama'),
        ),
        migrations.AddField(
            model_name='title',
            name='aciklama_tr',
            field=models.CharField(max_length=50, unique=True, null=True, verbose_name='A\xe7\u0131klama'),
        ),
    ]
