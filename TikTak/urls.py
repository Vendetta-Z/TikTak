from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as authViews
from . import views

ProductView = views.ProductView
RegAndLoginView = views.RegAndLoginView
Cart = views.Shop_сart

urlpatterns = [
    path('', ProductView.index, name='index'),
    path('<key>', ProductView.Shop_view_Category, name='Shop_cat'),
    path('<int:pk>/', ProductView.Shop_single_view, name='Shop_single'),
    path('Shop/', ProductView.Shop_view, name='Shop'),
    path('login/', RegAndLoginView.LoginView, name='login'),
    path('register/', RegAndLoginView.RegisterView, name='register'),
    path('logout/', authViews.LogoutView.as_view(next_page='index'), name='logout'),
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
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)