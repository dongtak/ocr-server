# Generated by Django 4.2.3 on 2023-07-31 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='image_url',
            field=models.URLField(default=''),
        ),
    ]