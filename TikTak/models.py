import datetime
import random

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User

from multiselectfield import MultiSelectField
from Like.models import Like


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    Product_name = models.CharField(max_length=200)
    product_description = models.CharField(max_length=500)
    Product_price = models.IntegerField(null=False)
    Product_color = models.CharField(max_length=20)
    Product_brand = models.CharField(max_length=100, default=None, null=False)
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
        ('Shorts', 'Шортики'),
        ('Dress', 'Платье'),
        ('Deaper', 'Пеленки'),
        ('Socks', 'Носки'),
        ('T-Shirts', 'Майки'),
        ('shoes', 'Обувь'),
    ]


    Product_Category = models.CharField(
        max_length=8,
        choices=P_Categorys,
        default='None',
    )

    for_which_gender = models.CharField(
        max_length=15,
        choices=[
            ('Boys', 'Для мальчиков'),
            ('Girls', 'Для девочек'),
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
            return 'None'
        return first_image.url


class ImageGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='TikTak/static/img', max_length=450)
    added_at = models.DateTimeField(auto_now_add=True)
    id = str(Product.id)+ str(added_at)


class Discount(models.Model):
    product = models.ForeignKey(Product,unique=True, on_delete=models.CASCADE, related_name='product')
    discount_percentage = models.IntegerField(null=False)
    when_set_discount_time = models.DateTimeField(auto_now=True)
    when_discount_time_out = models.IntegerField(null=False)

    def get_sale(self):
        product_price = self.product.Product_price
        product_price_discount_percentage = (product_price / 100) * self.discount_percentage
        return product_price - product_price_discount_percentage