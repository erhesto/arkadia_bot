# Generated by Django 3.1.4 on 2021-01-07 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20210107_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artifactdefinition',
            name='artifact_type',
            field=models.CharField(choices=[('WEAPON', 'bron'), ('ARMOR', 'zbroja'), ('JEWELRY', 'bizuteria')], max_length=96),
        ),
        migrations.AlterField(
            model_name='artifactdefinition',
            name='magic_power',
            field=models.CharField(choices=[('FIRE', 'Obrazenia od ognia'), ('MAGIC', 'Obrazenia od magii')], max_length=96),
        ),
    ]
