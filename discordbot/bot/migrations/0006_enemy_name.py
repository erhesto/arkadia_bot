# Generated by Django 3.1.4 on 2021-01-07 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_auto_20210107_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='enemy',
            name='name',
            field=models.CharField(default='1', max_length=256, unique=True),
            preserve_default=False,
        ),
    ]