# Generated by Django 3.2.6 on 2021-11-03 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TikTak', '0008_alter_product_added_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='ID_Product',
            new_name='id',
        ),
    ]
