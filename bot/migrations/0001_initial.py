# Generated by Django 3.1.4 on 2021-01-07 23:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enemy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('number_of_people', models.PositiveIntegerField(null=True)),
                ('toughness', models.CharField(choices=[('EASY', 'Latwy'), ('MEDIUM', 'Sredni'), ('HARD', 'Trudny'), ('ULTRA_HARD', 'Bardzo trudny'), ('EXTREME', 'Ekstremalnie ciezki')], max_length=32)),
                ('land', models.CharField(choices=[('TILEA', 'Tilea'), ('EMPIRE', 'Imperium'), ('WE_MOUNTAINS', 'Gory Kranca Swiata'), ('GREY_MOUNTAINS', 'Gory Szare'), ('BRETONIA', 'Bretonia')], max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MagicPower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='KeyDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short', models.CharField(db_index=True, max_length=64, unique=True)),
                ('description', models.TextField(null=True)),
                ('number_of_pieces', models.PositiveIntegerField(default=1)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.enemy')),
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
                ('durability_low', models.DateTimeField(auto_now_add=True)),
                ('durability_high', models.DateTimeField(auto_now_add=True)),
                ('exchanged', models.BooleanField(default=False)),
                ('exchanged_with', models.CharField(blank=True, max_length=256, null=True)),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.keydefinition')),
                ('dropped_from', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.enemy')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArtifactDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short', models.CharField(db_index=True, max_length=64, unique=True)),
                ('artifact_type', models.CharField(choices=[('WEAPON', 'bron'), ('ARMOR', 'zbroja'), ('JEWELRY', 'bizuteria')], max_length=96)),
                ('description', models.TextField()),
                ('magic_power', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.magicpower')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artifact',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('durability_low', models.DateTimeField(auto_now_add=True)),
                ('durability_high', models.DateTimeField(auto_now_add=True)),
                ('exchanged', models.BooleanField(default=False)),
                ('exchanged_with', models.CharField(blank=True, max_length=256, null=True)),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.artifactdefinition')),
                ('dropped_from', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.enemy')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
