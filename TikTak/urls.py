from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from Shop_cart.views import CartView as Cart
from . import views

ProductView = views.ProductView
RegAndLoginView = views.RegAndLoginView


urlpatterns = [
    path('', ProductView.index, name='index'),
    path('<int:pk>/', ProductView.shop_single_view, name='Shop_single'),
    path('Shop/', ProductView.shop_view, name='Shop'),
    path('login/', RegAndLoginView.login_view, name='login'),
    path('register/', RegAndLoginView.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]

urlpatterns += [
    path('cart/add/<int:ID_Product>/', Cart.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', Cart.item_clear, name='item_clear'),
    path('cart/item_remove/<key>/', Cart.item_remove, name='item_remove'),
    path('cart/item_increment/<key>/', Cart.item_increment, name='item_increment'),
    path('cart/item_decrement/<key>/', Cart.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', Cart.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', Cart.cart_detail, name='cart_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
