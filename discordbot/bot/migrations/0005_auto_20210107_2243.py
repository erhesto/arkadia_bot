# Generated by Django 3.1.4 on 2021-01-07 22:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_auto_20210107_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artifact',
            name='id',
        ),
        migrations.RemoveField(
            model_name='key',
            name='id',
        ),
        migrations.AddField(
            model_name='artifact',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='key',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='artifactdefinition',
            name='short',
            field=models.CharField(db_index=True, max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='keydefinition',
            name='short',
            field=models.CharField(db_index=True, max_length=64, unique=True),
        ),
    ]