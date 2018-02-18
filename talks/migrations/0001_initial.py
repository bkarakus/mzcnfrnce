# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import talks.models
from django.conf import settings
import mezzanine.core.fields
import utils.files


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='email address')),
                ('is_presenter', models.BooleanField(default=False)),
                ('profile', models.ForeignKey(blank=True, to='profiles.Profile', null=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1024)),
                ('abstract', models.FileField(upload_to=utils.files.get_abstracts_path, max_length=255, verbose_name='File', validators=[talks.models.validate_file_extension])),
                ('abstract_pdf', models.FileField(validators=[talks.models.validate_pdf_file], upload_to=utils.files.get_abstracts_path, max_length=255, blank=True, null=True, verbose_name='File (PDF)')),
                ('notes', models.TextField(help_text='Any notes for the conference organisers?', null=True, blank=True)),
                ('status', models.CharField(default=b'P', max_length=1, choices=[(b'A', b'Accepted'), (b'R', b'Not Accepted'), (b'P', b'Under Consideration'), (b'E', b'Not Submitted')])),
                ('fullpaper', models.FileField(validators=[talks.models.validate_pdf_file], upload_to=utils.files.get_fullpapers_path, max_length=255, blank=True, help_text=b'Only .pdf files', null=True, verbose_name='Full Paper')),
                ('fullpaper_pdf', models.FileField(validators=[talks.models.validate_pdf_file], upload_to=utils.files.get_fullpapers_path, max_length=255, blank=True, null=True, verbose_name='Full Paper (PDF)')),
                ('fullpaper_status', models.CharField(default=b'E', max_length=1, choices=[(b'A', b'Accepted'), (b'R', b'Not Accepted'), (b'P', b'Under Consideration'), (b'E', b'Not Submitted')])),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'permissions': (('view_all_talks', 'Can see all talks'),),
            },
        ),
        migrations.CreateModel(
            name='TalkSubject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=1024)),
                ('order', models.IntegerField(default=0)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'ordering': ('order', 'name'),
            },
        ),
        migrations.CreateModel(
            name='TalkType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=1024)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TalkUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=256)),
                ('url', models.URLField()),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
                ('talk', models.ForeignKey(to='talks.Talk')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='talk',
            name='talk_subject',
            field=models.ForeignKey(to='talks.TalkSubject', null=True),
        ),
        migrations.AddField(
            model_name='talk',
            name='talk_type',
            field=models.ForeignKey(to='talks.TalkType', null=True),
        ),
        migrations.AddField(
            model_name='talk',
            name='user',
            field=models.ForeignKey(related_name='talks', verbose_name='Author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='author',
            name='talk',
            field=models.ForeignKey(related_name='authors', to='talks.Talk'),
        ),
    ]
