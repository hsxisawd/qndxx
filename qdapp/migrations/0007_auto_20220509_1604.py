# Generated by Django 2.2.12 on 2022-05-09 08:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qdapp', '0006_auto_20220508_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='xinxi',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='xinxi',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
