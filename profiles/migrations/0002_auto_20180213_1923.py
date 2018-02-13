# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilespage',
            name='content_en',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='profilespage',
            name='content_tr',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
    ]
