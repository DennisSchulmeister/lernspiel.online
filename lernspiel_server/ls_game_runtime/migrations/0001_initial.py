# Generated by Django 5.0.6 on 2024-07-19 12:48

import django.db.models.deletion
import ls_game_runtime.models.game_id
import uuid
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
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('max_inactivity', models.SmallIntegerField(blank=True, default=1, help_text='Game execution will stop if no participant joins within this period. The game will be resumed once a participant joins. Zero means to never stop.', verbose_name='Max. Inactivity Minutes')),
                ('running', models.BooleanField(verbose_name='Currently Running')),
                ('channel', models.CharField(blank=True, max_length=255, verbose_name='Channel')),
                ('heartbeat', models.DateTimeField(blank=True, null=True, verbose_name='Heartbeat')),
                ('participants_count', models.IntegerField(blank=True, default=0, verbose_name='Current Participants')),
                ('participants_since', models.DateTimeField(blank=True, null=True, verbose_name='Last Join or Leave')),
                ('created_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ls_game_definition.gamedefinition', verbose_name='Game Definition')),
                ('modified_by', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modified By')),
            ],
            options={
                'verbose_name': 'Game Instance',
                'verbose_name_plural': 'Game Instances',
                'ordering': ['definition', 'created_at'],
            },
        ),
        migrations.CreateModel(
            name='GameId',
            fields=[
                ('id', models.CharField(default=ls_game_runtime.models.game_id.GameId._generate_game_id, editable=False, max_length=64, primary_key=True, serialize=False, verbose_name='Game ID')),
                ('participant_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ls_game_definition.participantrole', verbose_name='Participant Role')),
                ('game_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ls_game_runtime.gameinstance', verbose_name='Game Instance')),
            ],
            options={
                'verbose_name': 'Game ID',
                'verbose_name_plural': 'Game IDs',
                'ordering': ['id'],
            },
        ),
        migrations.AddIndex(
            model_name='gameinstance',
            index=models.Index(fields=['definition', 'running'], name='ls_game_run_definit_c3e130_idx'),
        ),
        migrations.AddIndex(
            model_name='gameinstance',
            index=models.Index(fields=['running', 'channel'], name='ls_game_run_running_9a5f22_idx'),
        ),
        migrations.AddIndex(
            model_name='gameinstance',
            index=models.Index(fields=['channel', 'running'], name='ls_game_run_channel_99a2a2_idx'),
        ),
    ]
