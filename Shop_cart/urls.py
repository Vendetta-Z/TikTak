from django.urls import path
from .views import CartView
from django.conf import settings


urlpatterns = [
    path('cart/add/<int:id>/', CartView.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', CartView.item_clear, name='item_clear'),
    path('cart/item_remove/<key>/', CartView.item_remove, name='item_remove'),
    path('cart/item_increment/<key>/', CartView.item_increment, name='item_increment'),
    path('cart/item_decrement/<key>/', CartView.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', CartView.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', CartView.cart_detail, name='cart_detail'),
]
