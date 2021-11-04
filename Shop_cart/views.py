from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Cart
from TikTak.models import Product


class CartView:

    @login_required(login_url="/users/login")
    def cart_add(self, id):
        cart = Cart(self)
        quantity = self.POST.get('quantity')
        size = self.POST.get('size')

        product = Product.objects.get(id=id)
        cart.add(product=product, quantity=quantity, size=size, color='black')
        cart.save()
        return redirect("Shop")

    @login_required(login_url="/users/login")
    def item_clear(self, id):
        cart = Cart(self)
        product = Product.objects.get(id=id)
        cart.remove(product)
        return redirect("cart_detail")

    @login_required(login_url="/users/login")
    def item_increment(self, key):
        cart = Cart(self)
        cart.increment(key=key)
        return redirect("cart_detail")

    @login_required(login_url="/users/login")
    def item_decrement(self, key):
        cart = Cart(self)
        cart.decrement(key=key)
        return redirect("cart_detail")

    @login_required(login_url="/users/login")
    def cart_clear(self):
        cart = Cart(self)
        cart.clear()
        return redirect("cart_detail")

    def cart_detail(self):
        a = []
        b = []
        cart = Cart(self).cart.items()
        for key, value in cart:
            a.append(value['quantity'])
            b.append(value['price'])

        quantity = [int(item) for item in a]
        price = [int(item) for item in b]

        total_sum = 0
        for i in range(len(quantity)):
            total_sum += quantity[i] * price[i]

        return render(self, 'cart/detail.html', {'total_sum': total_sum})

    @login_required(login_url='/users/login')
    def item_remove(self, key):
        cart = Cart(self)
        cart.remove(key=key)
        return redirect('cart_detail')
