import datetime
import random

from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    Product_name = models.CharField(max_length=200)
    product_description = models.CharField(max_length=500)
    Product_price = models.IntegerField()
    Product_color = models.CharField(max_length=20)
    Product_brand = models.CharField(max_length=100, default=None)
    Product_characteristics = models.CharField(max_length=1000)
    Added_time = models.DateTimeField(auto_now=True)
    likes = GenericRelation(Like)

    def __str__(self):
        return self.Product_name

    Choises = (
                ('0-3 месяца', '0-3'),
                ('3-6 месяцев', '3-6'),
                ('6-12 месяцев', '6-12'),
                ('12-18 месяцев', '12-18'),
                ('18-24 месяца', '18-24'),
                ('2 года', '2-y'),
                ('3 года', '3-y'),
                ('4 года', '4-y'),
                ('5 лет', '5-y'),
                ('6 лет', '6-y'),
                ('7 лет', '7-y'),
                ('8 лет', '8-y'),
                ('9 лет', '9-y'),
                ('10 лет', '10-y'),
                ('11 лет', '11-y'),
                ('12 лет', '12-y'),
                ('13 лет', '13-y'),
                ('14 лет (XS)', '14-y'),
                ('16 лет (S)', '16-y'),
                ('18 лет (M)', '18-y'),)

    Product_size = MultiSelectField(choices=Choises)

    P_Categorys = [
        ('Шортики', 'Shorts'),
        ('Платье', 'Dress'),
        ('Пеленки', 'Deaper'),
        ('Носки', 'Socks'),
        ('Майки', 'T-Shirts'),
        ('Обувь', 'shoes'),
    ]

    Product_Category = models.CharField(
        max_length=7,
        choices=P_Categorys,
        default='None',
    )

    for_which_gender = models.CharField(
        max_length=15,
        choices=[
            ('Для мальчиков', 'Boys'),
            ('Для девочек', 'Girls'),
        ],
        default=None,
    )

    @property
    def total_likes(self):
        return self.likes.count()

    def get_a_list_without_dublicate(self, attr_name):
        returned_list = []
        for product in Product.objects.all():
            attr_values = product.__getattribute__(attr_name)
            returned_list.append(attr_values)
        return set(returned_list)

    def get_recently_added_products(self, amount):
        return Product.objects.order_by('-Added_time')[:amount]

    def get_first_image(self):
        try:
            first_image = self.images.first().image
        except AttributeError:
            first_image = self
        return first_image


class ImageGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='TikTak/static/img')

