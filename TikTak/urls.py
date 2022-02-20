from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import ProductView, RegAndLoginView

urlpatterns = [
    path('', ProductView.index, name='index'),
    path('<int:pk>/', ProductView.shop_single_view, name='Shop_single'),
    path('Shop/', ProductView.shop_view, name='Shop'),
    path('favorite/', ProductView.favorite, name='favorite'),
    path('Profile/', ProductView.profile, name='Profile'),
    path('add_new_product/', ProductView.add_new_product, name='A_N_P'),
    path('DeleteProduct/', ProductView.DeleteProduct, name='DeleteProduct'),
    path('EditingProduct/<int:Product_id>', ProductView.EditingProduct, name='Product_edit'),
    path('EditingProduct_ajax/', ProductView.EditingProduct_ajax, name='Product_edit'),

    # path('ChangeProductImage/', ProductView.AddOrChangeProductImage , name='ChangeProductImage'),
    path('AddNewProductImage/', ProductView.addNewProductImage , name='addNewProductImage'),
    path('DeleteProductImage/', ProductView._delete_product_image_, name='DeleteProductImage'),
    path('ChangeProductImage/', ProductView.ChangeProductImage, name='ChangeProductImage'),

    path('login/', RegAndLoginView.login_view, name='login'),
    path('register/', RegAndLoginView.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    path('cart/', include('Shop_cart.urls')),
    path('Like/', include('Like.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
