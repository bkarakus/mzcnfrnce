# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('image', mezzanine.core.fields.FileField(max_length=255, null=True, verbose_name='Image', blank=True)),
                ('heading', models.CharField(default=b'Blurb for this featured image goes here.', max_length=60)),
                ('caption', models.CharField(default=b'Blurb for this featured image goes here.', max_length=100)),
            ],
            options={
                'ordering': ('_order',),
            },
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Page')),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('heading', models.CharField(default=b'Super Cool Heading', help_text=b'Heading for paragraph', max_length=100)),
                ('paragraph_blurb', models.CharField(default=b'This is a test. I am a robot.', help_text=b'Paragraph under the top heading', max_length=600)),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Home Page',
                'verbose_name_plural': 'Home Pages',
            },
            bases=('pages.page', models.Model),
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('image', mezzanine.core.fields.FileField(max_length=255, null=True, verbose_name='Image', blank=True)),
                ('heading', models.CharField(max_length=30)),
                ('caption', models.CharField(default=b'Blurb for image', max_length=100)),
                ('homepage', models.ForeignKey(related_name='slides', to='custom_pages.HomePage')),
            ],
            options={
                'ordering': ('_order',),
            },
        ),
        migrations.AddField(
            model_name='feature',
            name='homepage',
            field=models.ForeignKey(related_name='features', to='custom_pages.HomePage'),
        ),
    ]
