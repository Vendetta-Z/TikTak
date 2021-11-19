# Generated by Django 3.2.6 on 2021-11-19 14:10

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Product_name', models.CharField(max_length=200)),
                ('product_description', models.CharField(max_length=500)),
                ('Product_price', models.IntegerField()),
                ('Product_color', models.CharField(max_length=20)),
                ('Product_brand', models.CharField(default=None, max_length=100)),
                ('Product_characteristics', models.CharField(max_length=1000)),
                ('Added_time', models.DateTimeField(auto_now=True)),
                ('Product_size', multiselectfield.db.fields.MultiSelectField(choices=[('0-3 месяца', '0-3'), ('3-6 месяцев', '3-6'), ('6-12 месяцев', '6-12'), ('12-18 месяцев', '12-18'), ('18-24 месяца', '18-24'), ('2 года', '2-y'), ('3 года', '3-y'), ('4 года', '4-y'), ('5 лет', '5-y'), ('6 лет', '6-y'), ('7 лет', '7-y'), ('8 лет', '8-y'), ('9 лет', '9-y'), ('10 лет', '10-y'), ('11 лет', '11-y'), ('12 лет', '12-y'), ('13 лет', '13-y'), ('14 лет (XS)', '14-y'), ('16 лет (S)', '16-y'), ('18 лет (M)', '18-y')], max_length=175)),
                ('Product_Category', models.CharField(choices=[('Шортики', 'Shorts'), ('Платье', 'Dress'), ('Пеленки', 'Deaper'), ('Носки', 'Socks'), ('Майки', 'T-Shirts'), ('Обувь', 'shoes')], default='None', max_length=7)),
                ('for_which_gender', models.CharField(choices=[('Для мальчиков', 'Boys'), ('Для девочек', 'Girls')], default=None, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='ImageGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='TikTak/static/img')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='TikTak.product')),
            ],
        ),
    ]
