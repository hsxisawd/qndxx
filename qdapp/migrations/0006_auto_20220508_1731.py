# Generated by Django 2.2.12 on 2022-05-08 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qdapp', '0005_auto_20220507_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='num',
            name='qdlink',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='num',
            name='qishuname',
            field=models.CharField(max_length=250, null=True),
        ),
    ]