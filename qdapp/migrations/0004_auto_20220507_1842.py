# Generated by Django 2.2.12 on 2022-05-07 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qdapp', '0003_remove_student_studentnum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Num',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=1)),
            ],
        ),
        migrations.RenameField(
            model_name='fileid',
            old_name='fileif',
            new_name='fileid',
        ),
    ]
