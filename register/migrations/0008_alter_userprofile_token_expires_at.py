# Generated by Django 5.1.2 on 2024-11-28 08:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0007_remove_userprofile_spotify_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='token_expires_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]