# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields
from django.conf import settings
import django.core.validators
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'As you would like it to appear in the conference program.', max_length=100, null=True, validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z\\.\\-\\_\\ ]*$', message=b'Please use only English Alphabet', code=b'invalid_regex')])),
                ('biography', models.TextField(help_text=b"A little bit about you.  Edit using <a href='http://warpedvisions.org/projects/markdown-cheat-sheet/target='_blank'>Markdown</a>.", blank=True)),
                ('university', models.CharField(max_length=100, null=True, verbose_name='University', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z\\.\\-\\_\\ ]*$', message=b'Please use only English Alphabet', code=b'invalid_regex')])),
                ('department', models.CharField(max_length=100, null=True, verbose_name='Department', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z\\.\\-\\_\\ ]*$', message=b'Please use only English Alphabet', code=b'invalid_regex')])),
                ('country', django_countries.fields.CountryField(default=b'TR', max_length=2, verbose_name='Country')),
                ('phone', models.CharField(max_length=20, null=True, verbose_name='Phone')),
                ('photo', models.ImageField(upload_to=b'profile_photos', blank=True)),
                ('in_speakers_page', models.BooleanField(default=False)),
                ('in_participants_page', models.BooleanField(default=False)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProfilesPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Page')),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('content_en', mezzanine.core.fields.RichTextField(null=True, verbose_name='Content')),
                ('content_tr', mezzanine.core.fields.RichTextField(null=True, verbose_name='Content')),
                ('profile_type', models.CharField(max_length=1, verbose_name='Profile Type', choices=[(b'S', 'Speakers'), (b'P', 'Participants')])),
                ('per_page', models.SmallIntegerField(default=25, help_text='Number of profiles shown in the page.', verbose_name='Profiles per page')),
            ],
            options={
                'ordering': ('_order',),
            },
            bases=('pages.page', models.Model),
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aciklama', models.CharField(unique=True, max_length=50, verbose_name='A\xe7\u0131klama')),
                ('aciklama_en', models.CharField(max_length=50, unique=True, null=True, verbose_name='A\xe7\u0131klama')),
                ('aciklama_tr', models.CharField(max_length=50, unique=True, null=True, verbose_name='A\xe7\u0131klama')),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name': 'Title',
                'verbose_name_plural': 'Titles',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='title',
            field=models.ForeignKey(to='profiles.Title', null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(related_name='profile_list', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
