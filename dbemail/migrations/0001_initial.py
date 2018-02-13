# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_email', models.TextField(verbose_name='from email')),
                ('recipients', models.TextField(verbose_name='recipients')),
                ('subject', models.TextField(verbose_name='subject')),
                ('body', models.TextField(verbose_name='message')),
                ('ok', models.BooleanField(default=False, db_index=True, verbose_name='ok')),
                ('date_sent', models.DateTimeField(auto_now_add=True, verbose_name='date sent', db_index=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'ordering': ('-date_sent',),
                'verbose_name': 'email log',
                'verbose_name_plural': 'email logs',
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('base_template', models.CharField(help_text="If present, the name of a django template.<br/> The body field will be present as the 'email_body' context variable", max_length=1024, blank=True)),
                ('subject', models.CharField(max_length=1024)),
                ('from_address', models.CharField(help_text="Specify as: 'Full Name &lt;email@address>'<br/>Defaults to: 'no-reply@site.domain'", max_length=1024, null=True, blank=True)),
                ('body', models.TextField(default='')),
                ('txt_body', models.TextField(default='', help_text='If present, use as the plain-text body', verbose_name='Email Body')),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
