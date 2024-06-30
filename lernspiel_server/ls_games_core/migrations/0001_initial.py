# Generated by Django 5.0.6 on 2024-06-30 02:48

import django.db.models.deletion
import ls_games_core.models.meta
import ls_games_core.models.shared
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
            name='EventMeta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
                'ordering': ['parent', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('sort_order', models.SmallIntegerField(verbose_name='Sort Order')),
                ('created_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('modified_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ls_games_core.category', verbose_name='Parent Category')),
            ],
            options={
                'verbose_name': 'Meta: Category',
                'verbose_name_plural': 'Meta: Categories',
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='Category_T',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lernspiel_server.language')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_games_core.category')),
            ],
            options={
                'ordering': ['parent', 'language'],
            },
        ),
        migrations.CreateModel(
            name='EventMeta_T',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lernspiel_server.language')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_games_core.eventmeta')),
            ],
            options={
                'ordering': ['parent', 'language'],
            },
        ),
        migrations.CreateModel(
            name='EventParameterMeta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('data_type', models.CharField(choices=[('plain', 'Plain Text'), ('text', 'Formatted Text'), ('num', 'Number'), ('bool', 'Boolean'), ('dict', 'Dictionary')], max_length=10, verbose_name='')),
                ('length', models.PositiveSmallIntegerField(blank=True, verbose_name='Length')),
                ('is_array', models.BooleanField(verbose_name='Is Array')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='ls_games_core.eventmeta')),
            ],
            options={
                'verbose_name': 'Parameter',
                'verbose_name_plural': 'Parameters',
                'ordering': ['parent', 'name'],
            },
        ),
        migrations.CreateModel(
            name='EventParameterMeta_T',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lernspiel_server.language')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_games_core.eventparametermeta')),
            ],
            options={
                'ordering': ['parent', 'language'],
            },
        ),
        migrations.CreateModel(
            name='GameComponentMeta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('thumbnail', models.FileField(upload_to=ls_games_core.models.meta.GameComponentMeta._calc_file_path, verbose_name='Thumbnail')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ls_games_core.category', verbose_name='Category')),
                ('created_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('modified_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
            ],
            options={
                'verbose_name': 'Meta: Game Component',
                'verbose_name_plural': 'Meta: Game Components',
                'ordering': ['category', 'name'],
            },
        ),
        migrations.AddField(
            model_name='eventmeta',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='ls_games_core.gamecomponentmeta'),
        ),
        migrations.CreateModel(
            name='GameComponentMeta_T',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lernspiel_server.language')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_games_core.gamecomponentmeta')),
            ],
            options={
                'ordering': ['parent', 'language'],
            },
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('object_id', models.UUIDField()),
                ('file_data', models.FileField(upload_to=ls_games_core.models.shared.AbstractFileModel._calc_file_path, verbose_name='File Data')),
                ('file_name', models.CharField(max_length=255, verbose_name='File Name')),
                ('file_size', models.PositiveIntegerField(verbose_name='File Size')),
                ('mime_type', models.CharField(max_length=64, verbose_name='MIME Type')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('created_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('modified_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
            ],
            options={
                'verbose_name': 'Media File',
                'verbose_name_plural': 'Media Files',
                'ordering': ['content_type', 'object_id', 'file_name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PropertyMeta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('data_type', models.CharField(choices=[('plain', 'Plain Text'), ('text', 'Formatted Text'), ('num', 'Number'), ('bool', 'Boolean'), ('dict', 'Dictionary')], max_length=10, verbose_name='')),
                ('length', models.PositiveSmallIntegerField(blank=True, verbose_name='Length')),
                ('is_array', models.BooleanField(verbose_name='Is Array')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='ls_games_core.gamecomponentmeta')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
                'ordering': ['parent', 'name'],
            },
        ),
        migrations.CreateModel(
            name='PropertyMeta_T',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lernspiel_server.language')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_games_core.propertymeta')),
            ],
            options={
                'ordering': ['parent', 'language'],
            },
        ),
        migrations.CreateModel(
            name='SlotMeta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='ls_games_core.gamecomponentmeta')),
            ],
            options={
                'verbose_name': 'Slot',
                'verbose_name_plural': 'Slots',
                'ordering': ['parent', 'name'],
            },
        ),
        migrations.CreateModel(
            name='SlotMeta_T',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lernspiel_server.language')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_games_core.slotmeta')),
            ],
            options={
                'ordering': ['parent', 'language'],
            },
        ),
        migrations.CreateModel(
            name='SourceFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('object_id', models.UUIDField()),
                ('file_data', models.FileField(upload_to=ls_games_core.models.shared.AbstractFileModel._calc_file_path, verbose_name='File Data')),
                ('file_name', models.CharField(max_length=255, verbose_name='File Name')),
                ('file_size', models.PositiveIntegerField(verbose_name='File Size')),
                ('mime_type', models.CharField(max_length=64, verbose_name='MIME Type')),
                ('source_type', models.CharField(choices=[('html', 'HTML Template'), ('css', 'CSS Stylesheet'), ('js', 'JS Source File'), ('script', 'Game Script')], max_length=10, verbose_name='Source Type')),
                ('sort_order', models.SmallIntegerField(verbose_name='Sort Order')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('created_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('modified_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
            ],
            options={
                'verbose_name': 'Source File',
                'verbose_name_plural': 'Source Files',
                'ordering': ['content_type', 'object_id', 'source_type', 'sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['parent', 'sort_order'], name='ls_games_co_parent__2f0212_idx'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['parent', 'name'], name='ls_games_co_parent__9f9fda_idx'),
        ),
        migrations.AddIndex(
            model_name='category_t',
            index=models.Index(fields=['parent', 'language'], name='ls_games_co_parent__86372c_idx'),
        ),
        migrations.AddIndex(
            model_name='eventmeta_t',
            index=models.Index(fields=['parent', 'language'], name='ls_games_co_parent__fa0244_idx'),
        ),
        migrations.AddIndex(
            model_name='eventparametermeta',
            index=models.Index(fields=['parent', 'name'], name='ls_games_co_parent__c4a08f_idx'),
        ),
        migrations.AddIndex(
            model_name='eventparametermeta_t',
            index=models.Index(fields=['parent', 'language'], name='ls_games_co_parent__c0df4f_idx'),
        ),
        migrations.AddIndex(
            model_name='gamecomponentmeta',
            index=models.Index(fields=['name'], name='ls_games_co_name_b8191f_idx'),
        ),
        migrations.AddIndex(
            model_name='eventmeta',
            index=models.Index(fields=['parent', 'name'], name='ls_games_co_parent__f25f5e_idx'),
        ),
        migrations.AddIndex(
            model_name='gamecomponentmeta_t',
            index=models.Index(fields=['parent', 'language'], name='ls_games_co_parent__e72f1f_idx'),
        ),
        migrations.AddIndex(
            model_name='mediafile',
            index=models.Index(fields=['content_type', 'object_id', 'file_name'], name='ls_games_co_content_f98ddb_idx'),
        ),
        migrations.AddIndex(
            model_name='propertymeta',
            index=models.Index(fields=['parent', 'name'], name='ls_games_co_parent__e757b8_idx'),
        ),
        migrations.AddIndex(
            model_name='propertymeta_t',
            index=models.Index(fields=['parent', 'language'], name='ls_games_co_parent__b678b3_idx'),
        ),
        migrations.AddIndex(
            model_name='slotmeta',
            index=models.Index(fields=['parent', 'name'], name='ls_games_co_parent__24faa6_idx'),
        ),
        migrations.AddIndex(
            model_name='slotmeta_t',
            index=models.Index(fields=['parent', 'language'], name='ls_games_co_parent__1f908c_idx'),
        ),
        migrations.AddIndex(
            model_name='sourcefile',
            index=models.Index(fields=['content_type', 'object_id', 'file_name'], name='ls_games_co_content_444eb3_idx'),
        ),
        migrations.AddIndex(
            model_name='sourcefile',
            index=models.Index(fields=['content_type', 'object_id', 'source_type', 'sort_order'], name='ls_games_co_content_e1790d_idx'),
        ),
    ]
