# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import articles.models
import django.utils.timezone
from django.conf import settings
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique_for_year=b'publish_date')),
                ('keywords', models.TextField(help_text='If omitted, the keywords will be the same as the article tags.', blank=True)),
                ('description', models.TextField(help_text="If omitted, the description will be determined by the first bit of the article's content.", blank=True)),
                ('markup', models.CharField(default=b'h', help_text='Select the type of markup you are using in this article.\n<ul>\n<li><a href="http://daringfireball.net/projects/markdown/basics" target="_blank">Markdown Guide</a></li>\n<li><a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html" target="_blank">ReStructured Text Guide</a></li>\n<li><a href="http://thresholdstate.com/articles/4312/the-textile-reference-manual" target="_blank">Textile Guide</a></li>\n</ul>', max_length=1, choices=[(b'h', 'HTML/Plain Text'), (b'm', 'Markdown'), (b'r', 'ReStructured Text'), (b't', 'Textile')])),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('rendered_content', models.TextField()),
                ('auto_tag', models.BooleanField(default=True, help_text='Check this if you want to automatically assign any existing tags to this article based on its content.')),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now, help_text='The date and time this article shall appear online.')),
                ('expiration_date', models.DateTimeField(help_text='Leave blank if the article does not expire.', null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('login_required', models.BooleanField(help_text='Enable this if users must login before they can read this article.')),
                ('use_addthis_button', models.BooleanField(default=True, help_text='Check this to show an AddThis bookmark button when viewing an article.', verbose_name='Show AddThis button')),
                ('addthis_use_author', models.BooleanField(default=True, help_text="Check this if you want to use the article author's username for the AddThis button.  Respected only if the username field is left empty.", verbose_name="Use article author's username")),
                ('addthis_username', models.CharField(default=None, help_text='The AddThis username to use for the button.', max_length=50, verbose_name='AddThis Username', blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('followup_for', models.ManyToManyField(help_text='Select any other articles that this article follows up on.', related_name='followups', to='articles.Article', blank=True)),
                ('related_articles', models.ManyToManyField(related_name='related_articles_rel_+', to='articles.Article', blank=True)),
                ('sites', models.ManyToManyField(to='sites.Site', blank=True)),
            ],
            options={
                'ordering': ('-publish_date', 'title'),
                'get_latest_by': 'publish_date',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('ordering', models.IntegerField(default=0)),
                ('is_live', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('ordering', 'name'),
                'verbose_name_plural': 'Article statuses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachment', models.FileField(upload_to=articles.models.upload_to)),
                ('caption', models.CharField(max_length=255, blank=True)),
                ('article', models.ForeignKey(related_name='attachments', to='articles.Article')),
            ],
            options={
                'ordering': ('-article', 'id'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('slug', models.CharField(max_length=64, unique=True, null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.ForeignKey(to='articles.ArticleStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(help_text='Tags that describe this article, comma separated when input into admin.', to='articles.Tag', blank=True),
            preserve_default=True,
        ),
    ]
