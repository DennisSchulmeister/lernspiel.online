# Generated by Django 5.0.6 on 2024-06-27 19:07

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import lernspiel_server.db
import lernspiel_server.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='Id')),
                ('domain', models.CharField(max_length=100, verbose_name='Domain Name')),
                ('name', models.CharField(max_length=255, verbose_name='Display Name')),
                ('logo', models.FileField(upload_to=lernspiel_server.models.Site._calc_file_path, verbose_name='Logo Image')),
                ('logo_width', models.CharField(default='20em', max_length=20, verbose_name='Logo Width')),
                ('header_bg', models.CharField(default='#234769', max_length=100, verbose_name='Header Background')),
                ('link_color', models.CharField(default='crimson', max_length=20, verbose_name='Link Color')),
            ],
            options={
                'verbose_name': 'Website',
                'verbose_name_plural': 'Websites',
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
            ],
            options={
                'verbose_name': 'User Group',
                'verbose_name_plural': 'User Groups',
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.SmallIntegerField(choices=[(0, 'Regular User'), (1, 'Developer'), (2, 'Application')], default=0, verbose_name='User Type')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('date_expires', models.DateTimeField(blank=True, null=True, verbose_name='Expiry Date')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('object_id', models.UUIDField()),
                ('file', models.FileField(upload_to=lernspiel_server.models.MediaFile._calc_file_path, verbose_name='File')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Media File',
                'verbose_name_plural': 'Media Files',
                'ordering': ['file'],
                'indexes': [models.Index(fields=['content_type', 'object_id'], name='lernspiel_s_content_4c4f13_idx')],
            },
            bases=(models.Model, lernspiel_server.db.CreatedModifiedByMixin),
        ),
    ]
