# Generated by Django 5.0.6 on 2024-07-19 12:48

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('lernspiel_server', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Background',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('created_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('modified_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
            ],
            options={
                'verbose_name': 'Background',
                'verbose_name_plural': 'Backgrounds',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CustomCSS',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('object_id', models.UUIDField()),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('position', models.PositiveSmallIntegerField(verbose_name='Position')),
                ('css_code', models.TextField(blank=True, null=True, verbose_name='CSS Code')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Custom Stylesheet',
                'verbose_name_plural': 'Custom Stylesheets',
                'ordering': ['name', 'position'],
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('created_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('modified_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menus',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Menu_T',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lernspiel_server.language')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_ui_static_pages.menu')),
            ],
            options={
                'verbose_name': 'Translation',
                'verbose_name_plural': 'Translations',
                'ordering': ['parent', 'language'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MenuAssignment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('object_id', models.UUIDField()),
                ('area', models.CharField(choices=[('header', 'Header'), ('footer', 'Footer')], max_length=10, verbose_name='Area')),
                ('position', models.PositiveSmallIntegerField(verbose_name='Position')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ls_ui_static_pages.menu', verbose_name='Menu')),
            ],
            options={
                'verbose_name': 'Menu Assignment',
                'verbose_name_plural': 'Menu Assignments',
                'ordering': ['area', 'menu'],
            },
        ),
        migrations.CreateModel(
            name='MenuEntry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('position', models.PositiveSmallIntegerField(verbose_name='Position')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('link_type', models.CharField(choices=[('none', 'None / Section Title'), ('url', 'Static URL address'), ('page', 'Text Page'), ('view', 'Built-In View')], default='none', max_length=10, verbose_name='Link type')),
                ('link_url', models.URLField(blank=True, verbose_name='URL')),
                ('link_view_name', models.CharField(blank=True, max_length=30, verbose_name='View Name')),
                ('link_view_par1', models.CharField(blank=True, max_length=30, verbose_name='Parameters')),
                ('link_view_par2', models.CharField(blank=True, max_length=30, verbose_name='')),
                ('link_view_par3', models.CharField(blank=True, max_length=30, verbose_name='')),
                ('link_view_par4', models.CharField(blank=True, max_length=30, verbose_name='')),
                ('link_view_par5', models.CharField(blank=True, max_length=30, verbose_name='')),
                ('new_window', models.BooleanField(verbose_name='Open in new window or tab')),
                ('login_status', models.CharField(choices=[('any', 'Show always'), ('logged-in', 'Show only for logged in users'), ('logged-out', 'Show only for logged out users')], default='any', max_length=10, verbose_name='Login Status')),
                ('created_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_entries', to='ls_ui_static_pages.menu', verbose_name='Menu')),
                ('modified_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
            ],
            options={
                'verbose_name': 'Menu Entry',
                'verbose_name_plural': 'Menu Entries',
                'ordering': ['menu', 'position'],
            },
        ),
        migrations.CreateModel(
            name='MenuEntry_T',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lernspiel_server.language')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_ui_static_pages.menuentry')),
            ],
            options={
                'verbose_name': 'Translation',
                'verbose_name_plural': 'Translations',
                'ordering': ['parent', 'language'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PageType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('template', models.CharField(choices=[('ls_ui_text_pages/pagetype/standard.html', 'Standard Text Page'), ('ls_ui_text_pages/pagetype/centered.html', 'Centered Content'), ('ls_ui_text_pages/pagetype/fullscreen.html', 'Fullscreen Content')], max_length=255, verbose_name='Template')),
                ('background', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ls_ui_static_pages.background', verbose_name='Background')),
                ('created_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('modified_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
            ],
            options={
                'verbose_name': 'Page  Type',
                'verbose_name_plural': 'Page Types',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PageType_T',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lernspiel_server.language')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_ui_static_pages.pagetype')),
            ],
            options={
                'verbose_name': 'Translation',
                'verbose_name_plural': 'Translations',
                'ordering': ['parent', 'language'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Name')),
                ('created_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('modified_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
            ],
            options={
                'verbose_name': 'Snippet',
                'verbose_name_plural': 'Snippets',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Snippet_T',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('format', models.CharField(choices=[('plain', 'Plain Text'), ('html', 'HTML'), ('markdown', 'Markdown')], max_length=10, verbose_name='Format')),
                ('content', models.TextField(blank=True, verbose_name='Content')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lernspiel_server.language')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_ui_static_pages.snippet')),
            ],
            options={
                'verbose_name': 'Translation',
                'verbose_name_plural': 'Translations',
                'ordering': ['parent', 'language'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TextPage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('url', models.CharField(max_length=255, verbose_name='URL')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('show_title', models.BooleanField(default=True, verbose_name='Show title on page')),
                ('login_required', models.BooleanField(default=False, verbose_name='Login Required')),
                ('published', models.BooleanField(default=False, verbose_name='Publish Page')),
                ('publish_start', models.DateField(blank=True, null=True, verbose_name='Publish On')),
                ('publish_end', models.DateField(blank=True, null=True, verbose_name='Publish Until')),
                ('background', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ls_ui_static_pages.background', verbose_name='Background')),
                ('created_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('modified_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
                ('page_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ls_ui_static_pages.pagetype', verbose_name='Page Type')),
            ],
            options={
                'verbose_name': 'Text Page',
                'verbose_name_plural': 'Text Pages',
                'ordering': ['url'],
            },
        ),
        migrations.AddField(
            model_name='menuentry',
            name='link_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ls_ui_static_pages.textpage'),
        ),
        migrations.CreateModel(
            name='TextPage_T',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('format', models.CharField(choices=[('plain', 'Plain Text'), ('html', 'HTML'), ('markdown', 'Markdown')], max_length=10, verbose_name='Format')),
                ('content', models.TextField(blank=True, verbose_name='Content')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lernspiel_server.language')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_ui_static_pages.textpage')),
            ],
            options={
                'verbose_name': 'Translation',
                'verbose_name_plural': 'Translations',
                'ordering': ['parent', 'language'],
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='background',
            index=models.Index(fields=['name'], name='ls_ui_stati_name_06fd57_idx'),
        ),
        migrations.AddIndex(
            model_name='menu',
            index=models.Index(fields=['name'], name='ls_ui_stati_name_10b2fb_idx'),
        ),
        migrations.AddIndex(
            model_name='menu_t',
            index=models.Index(fields=['parent', 'language'], name='ls_ui_stati_parent__914ac4_idx'),
        ),
        migrations.AddIndex(
            model_name='menuentry_t',
            index=models.Index(fields=['parent', 'language'], name='ls_ui_stati_parent__651515_idx'),
        ),
        migrations.AddIndex(
            model_name='pagetype',
            index=models.Index(fields=['name'], name='ls_ui_stati_name_bf2c22_idx'),
        ),
        migrations.AddIndex(
            model_name='pagetype_t',
            index=models.Index(fields=['parent', 'language'], name='ls_ui_stati_parent__763e53_idx'),
        ),
        migrations.AddIndex(
            model_name='snippet',
            index=models.Index(fields=['name'], name='ls_ui_stati_name_bdb53a_idx'),
        ),
        migrations.AddIndex(
            model_name='snippet_t',
            index=models.Index(fields=['parent', 'language'], name='ls_ui_stati_parent__4213d5_idx'),
        ),
        migrations.AddIndex(
            model_name='textpage',
            index=models.Index(fields=['url'], name='ls_ui_stati_url_970ae0_idx'),
        ),
        migrations.AddIndex(
            model_name='menuentry',
            index=models.Index(fields=['name'], name='ls_ui_stati_name_033569_idx'),
        ),
        migrations.AddIndex(
            model_name='textpage_t',
            index=models.Index(fields=['parent', 'language'], name='ls_ui_stati_parent__09c709_idx'),
        ),
    ]
