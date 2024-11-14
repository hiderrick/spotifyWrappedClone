# Generated by Django 5.1.2 on 2024-11-13 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_spotifywrap_theme_spotifywrap_time_range_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='spotifywrap',
            name='name',
            field=models.CharField(default='No Name', max_length=255),
        ),
        migrations.AlterField(
            model_name='spotifywrap',
            name='theme',
            field=models.CharField(choices=[('halloween', 'Halloween'), ('christmas', 'Christmas')], max_length=20),
        ),
        migrations.AlterField(
            model_name='spotifywrap',
            name='time_range',
            field=models.CharField(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], max_length=10),
        ),
    ]