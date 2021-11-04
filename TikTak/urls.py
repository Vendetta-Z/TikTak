from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from like.services import *

ProductView = views.ProductView
RegAndLoginView = views.RegAndLoginView


urlpatterns = [
    path('', ProductView.index, name='index'),
    path('<int:pk>/', ProductView.shop_single_view, name='Shop_single'),
    path('Shop/', ProductView.shop_view, name='Shop'),
    path('login/', RegAndLoginView.login_view, name='login'),
    path('register/', RegAndLoginView.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('cart/', include('Shop_cart.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
