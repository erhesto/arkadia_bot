# Generated by Django 3.1.4 on 2021-01-07 20:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artifact',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artifact',
            name='dropped_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.enemy'),
        ),
        migrations.AddField(
            model_name='artifact',
            name='durability_high',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artifact',
            name='durability_low',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artifact',
            name='exchanged',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='artifact',
            name='exchanged_with',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='key',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='key',
            name='dropped_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.enemy'),
        ),
        migrations.AddField(
            model_name='key',
            name='durability_high',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='key',
            name='durability_low',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='key',
            name='exchanged',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='key',
            name='exchanged_with',
            field=models.CharField(max_length=256, null=True),
        ),
    ]