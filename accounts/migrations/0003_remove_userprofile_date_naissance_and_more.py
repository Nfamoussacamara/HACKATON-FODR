# Generated by Django 5.2.1 on 2025-05-14 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_problem_userprofile_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='date_naissance',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='photo_signal',
        ),
        migrations.AddField(
            model_name='problem',
            name='image_problem',
            field=models.ImageField(blank=True, null=True, upload_to='problem/'),
        ),
    ]
