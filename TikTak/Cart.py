from django.conf import settings
from django.db import models
from random import randint

class Cart(models.Model):

    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity, size, color, action=None):
        """
        Add a product to the cart or update its quantity.
        """
        id_Product = product.ID_Product
        r = randint(1, 5000)
        cart_item_product = (id_Product * id_Product) / 2 * r
        if cart_item_product in self.cart:
            cart_item_product / 2 * r

        newItem = True

        if str(product.ID_Product) not in self.cart.keys():
            self.cart[cart_item_product] = {
                'userid': self.request.user.id,
                'product_id': id_Product,
                'name': product.Product_name,
                'description': product.product_description,
                'brand': product.Product_brand,
                'quantity': quantity,
                'size': size,
                'color': color,
                'price': product.Product_price,
                'image': product.Product_image.url,
            }
            print(self.cart)

            self.save()
        elif size not in self.cart.values():
            self.cart[cart_item_product] = {
                'userid': self.request.user.id,
                'product_id': id,
                'name': product.Product_name,
                'description': product.product_description,
                'brand': product.Product_brand,
                'quantity': quantity,
                'size': size,
                'color': color,
                'price': product.Product_price,
                'image': product.Product_image.url,
            }
            print(self.cart + '\n')
            self.save()

        else:

            newItem = True

            self.cart.increment()
            if newItem == True:
                self.cart[product.ID_Product] = {
                    'userid': self.request.user.id,
                    'product_id': id,
                    'name': product.Product_name,
                    'quantity': 1,
                    'size': size,
                    'price': str(product.Product_price),
                    'image': product.Product_image.url
                }

        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, key):
        """
        Remove a product from the cart.
        """
        for key in self.cart:
            if key in self.cart:
                del self.cart[key]
                self.save()
                break

    def increment(self, key):
        a = self.cart[key]
        quantity = a['quantity']
        quantity = int(quantity) + 1
        a['quantity'] = quantity
        self.save()

    def decrement(self, key):

        a = self.cart[key]
        quantity = a['quantity']
        if(int(quantity) > 1):
            quantity = int(quantity) - 1
            a['quantity'] = quantity
            self.save()



    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
