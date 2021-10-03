from django.db import models

class Product(models.Model):
    ID_Product = models.AutoField(primary_key=True)
    Product_name = models.CharField(max_length=200)
    product_description = models.CharField(max_length=500)
    Product_price = models.IntegerField()
    Product_image = models.ImageField(blank=True, upload_to='TikTak/static/img/')
    Product_color = models.CharField(max_length=20)
    Product_brand = models.CharField(max_length=100, default=None)
    Product_size = models.CharField(max_length=30, default='None')
    Product_characteristics = models.CharField(max_length=1000)

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
        default='Шортики',
    )

    for_which_gender = models.CharField(
        max_length=15,
        choices=[
            ('Для мальчиков', 'Boys'),
            ('Для девочек', 'Girls'),
        ],
        default=None,
    )

    def __str__(self):
        return self.Product_name


    def get_a_list_without_dublicate(self, f):
        returned_list = []
        for product in Product.objects.all():
            a = (product.__getattribute__(f))
            for i in a:
                print(i)
            returned_list.append(a)
        return set(returned_list)

    def Product_item_in_list(self, str):
        size = str.split(' ')
        return list(size)

