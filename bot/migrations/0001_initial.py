# Generated by Django 3.1.4 on 2021-01-17 12:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArtifactDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short', models.CharField(db_index=True, max_length=120, unique=True)),
                ('description', models.TextField(blank=True, default='')),
                ('magic_power', models.CharField(max_length=256)),
                ('artifact_type', models.CharField(blank=True, choices=[('WEAPON', 'bron'), ('ARMOR', 'zbroja'), ('JEWELRY', 'bizuteria')], default='', max_length=96)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KeyDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short', models.CharField(db_index=True, max_length=120, unique=True)),
                ('description', models.TextField(blank=True, default='')),
                ('number_of_pieces', models.PositiveIntegerField(default=1)),
                ('destination', models.CharField(max_length=256)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('durability_low', models.DateTimeField(default=django.utils.timezone.now)),
                ('durability_high', models.DateTimeField(default=django.utils.timezone.now)),
                ('origin', models.CharField(max_length=256)),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.keydefinition')),
            ],
            options={
                'ordering': ['-durability_low'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artifact',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('durability_low', models.DateTimeField(default=django.utils.timezone.now)),
                ('durability_high', models.DateTimeField(default=django.utils.timezone.now)),
                ('origin', models.CharField(max_length=256)),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.artifactdefinition')),
            ],
            options={
                'ordering': ['-durability_low'],
                'abstract': False,
            },
        ),
    ]
