# Generated by Django 4.2.3 on 2023-07-31 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('bNum', models.AutoField(auto_created=1000, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField(blank=True, max_length=3000, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('modifiedAt', models.DateTimeField(auto_now=True, verbose_name='수정일')),
            ],
        ),
    ]
