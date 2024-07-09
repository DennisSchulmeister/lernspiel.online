# Generated by Django 5.0.6 on 2024-07-09 22:36

import django.db.models.deletion
import ls_game_runtime.models.game_instance
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ls_game_definition', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameInstance',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('id', models.CharField(default=ls_game_runtime.models.game_instance.GameInstance._generate_game_id, editable=False, max_length=64, primary_key=True, serialize=False, verbose_name='Game ID')),
                ('running', models.BooleanField(verbose_name='Currently Running')),
                ('channel', models.CharField(blank=True, max_length=255, verbose_name='Channel')),
                ('heartbeat', models.DateTimeField(blank=True, null=True, verbose_name='Heartbeat')),
                ('created_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ls_game_definition.gamedefinition', verbose_name='Game Definition')),
                ('modified_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
            ],
            options={
                'verbose_name': 'Game Instance',
                'verbose_name_plural': 'Game Instances',
                'ordering': ['definition', 'created_at'],
                'indexes': [models.Index(fields=['definition', 'running'], name='ls_game_run_definit_c3e130_idx'), models.Index(fields=['running', 'channel'], name='ls_game_run_running_9a5f22_idx'), models.Index(fields=['channel', 'running'], name='ls_game_run_channel_99a2a2_idx')],
            },
        ),
    ]
