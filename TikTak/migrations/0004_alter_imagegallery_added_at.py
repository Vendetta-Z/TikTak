# Generated by Django 3.2.6 on 2022-01-25 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TikTak', '0003_imagegallery_added_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagegallery',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
