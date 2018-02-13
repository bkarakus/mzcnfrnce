# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('custom_pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='caption_en',
            field=models.CharField(default=b'Blurb for this featured image goes here.', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='feature',
            name='caption_tr',
            field=models.CharField(default=b'Blurb for this featured image goes here.', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='feature',
            name='heading_en',
            field=models.CharField(default=b'Blurb for this featured image goes here.', max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='feature',
            name='heading_tr',
            field=models.CharField(default=b'Blurb for this featured image goes here.', max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='content_en',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='content_tr',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='slide',
            name='caption_en',
            field=models.CharField(default=b'Blurb for image', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='slide',
            name='caption_tr',
            field=models.CharField(default=b'Blurb for image', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='slide',
            name='heading_en',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='slide',
            name='heading_tr',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
