# Generated by Django 5.0.6 on 2024-07-09 22:36

import django.db.models.deletion
import ls_game_meta.models.game_component
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
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
                ('position', models.SmallIntegerField(verbose_name='Position')),
                ('created_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('modified_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ls_game_meta.category', verbose_name='Parent Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Category_T',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lernspiel_server.language')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_game_meta.category')),
            ],
            options={
                'verbose_name': 'Translation',
                'verbose_name_plural': 'Translations',
                'ordering': ['parent', 'language'],
            },
        ),
        migrations.CreateModel(
            name='EventMeta_T',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lernspiel_server.language')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_game_meta.eventmeta')),
            ],
            options={
                'verbose_name': 'Translation',
                'verbose_name_plural': 'Translations',
                'ordering': ['parent', 'language'],
            },
        ),
        migrations.CreateModel(
            name='EventParameterMeta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('data_type', models.CharField(choices=[('plain', 'Plain Text'), ('text', 'Formatted Text'), ('num', 'Number'), ('bool', 'Boolean'), ('dict', 'Dictionary')], max_length=10, verbose_name='Data Type')),
                ('length', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Length')),
                ('is_array', models.BooleanField(verbose_name='Is Array')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='ls_game_meta.eventmeta')),
            ],
            options={
                'verbose_name': 'Event Parameter',
                'verbose_name_plural': 'Event Parameters',
            },
        ),
        migrations.CreateModel(
            name='EventParameterMeta_T',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lernspiel_server.language')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_game_meta.eventparametermeta')),
            ],
            options={
                'verbose_name': 'Translation',
                'verbose_name_plural': 'Translations',
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
                ('thumbnail', models.FileField(blank=True, null=True, upload_to=ls_game_meta.models.game_component.GameComponentMeta._calc_file_path, verbose_name='Thumbnail')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ls_game_meta.category', verbose_name='Category')),
                ('created_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('modified_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
            ],
            options={
                'verbose_name': 'Game Component',
                'verbose_name_plural': 'Game Components',
                'ordering': ['category', 'name'],
            },
        ),
        migrations.AddField(
            model_name='eventmeta',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='ls_game_meta.gamecomponentmeta'),
        ),
        migrations.CreateModel(
            name='GameComponentMeta_T',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lernspiel_server.language')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_game_meta.gamecomponentmeta')),
            ],
            options={
                'verbose_name': 'Translation',
                'verbose_name_plural': 'Translations',
                'ordering': ['parent', 'language'],
            },
        ),
        migrations.CreateModel(
            name='PropertyMeta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('data_type', models.CharField(choices=[('plain', 'Plain Text'), ('text', 'Formatted Text'), ('num', 'Number'), ('bool', 'Boolean'), ('dict', 'Dictionary')], max_length=10, verbose_name='Data Type')),
                ('length', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Length')),
                ('is_array', models.BooleanField(verbose_name='Is Array')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='ls_game_meta.gamecomponentmeta')),
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
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_game_meta.propertymeta')),
            ],
            options={
                'verbose_name': 'Translation',
                'verbose_name_plural': 'Translations',
                'ordering': ['parent', 'language'],
            },
        ),
        migrations.CreateModel(
            name='SlotMeta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='ls_game_meta.gamecomponentmeta')),
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
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ls_game_meta.slotmeta')),
            ],
            options={
                'verbose_name': 'Translation',
                'verbose_name_plural': 'Translations',
                'ordering': ['parent', 'language'],
            },
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['parent', 'position'], name='ls_game_met_parent__7b8248_idx'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['parent', 'name'], name='ls_game_met_parent__495c3d_idx'),
        ),
        migrations.AddIndex(
            model_name='category_t',
            index=models.Index(fields=['parent', 'language'], name='ls_game_met_parent__12d373_idx'),
        ),
        migrations.AddIndex(
            model_name='eventmeta_t',
            index=models.Index(fields=['parent', 'language'], name='ls_game_met_parent__628d61_idx'),
        ),
        migrations.AddIndex(
            model_name='eventparametermeta',
            index=models.Index(fields=['parent', 'name'], name='ls_game_met_parent__79e7a6_idx'),
        ),
        migrations.AddIndex(
            model_name='eventparametermeta_t',
            index=models.Index(fields=['parent', 'language'], name='ls_game_met_parent__27c747_idx'),
        ),
        migrations.AddIndex(
            model_name='gamecomponentmeta',
            index=models.Index(fields=['name'], name='ls_game_met_name_84c671_idx'),
        ),
        migrations.AddIndex(
            model_name='eventmeta',
            index=models.Index(fields=['parent', 'name'], name='ls_game_met_parent__4ce52b_idx'),
        ),
        migrations.AddIndex(
            model_name='gamecomponentmeta_t',
            index=models.Index(fields=['parent', 'language'], name='ls_game_met_parent__03311a_idx'),
        ),
        migrations.AddIndex(
            model_name='propertymeta',
            index=models.Index(fields=['parent', 'name'], name='ls_game_met_parent__336494_idx'),
        ),
        migrations.AddIndex(
            model_name='propertymeta_t',
            index=models.Index(fields=['parent', 'language'], name='ls_game_met_parent__8984ea_idx'),
        ),
        migrations.AddIndex(
            model_name='slotmeta',
            index=models.Index(fields=['parent', 'name'], name='ls_game_met_parent__f36c8c_idx'),
        ),
        migrations.AddIndex(
            model_name='slotmeta_t',
            index=models.Index(fields=['parent', 'language'], name='ls_game_met_parent__cf36ee_idx'),
        ),
    ]
