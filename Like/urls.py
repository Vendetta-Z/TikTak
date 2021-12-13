from django.urls import path
from . import views
DynamicProductView = views.DynamicProductView

urlpatterns = [
    path('add_like/', DynamicProductView.add_like, name='add_product_like'),
    path('is_liked/', DynamicProductView.is_liked, name='is_liked'),
]