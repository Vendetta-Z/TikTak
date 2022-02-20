from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


from Like.models import Like
from Shop_cart.models import Cart

from .models import Product, ImageGallery
from .RegAndLogin_services import _registration_user_, _login_user_
from .Product_services import _get_a_product_list_without_dublicate, _get_user_liked_products_, _get_filtered_products_, \
    _get_product_pagination_, _delete_product_, _add_new_product_, _change_product_image_, _editing_product_, _add_product_image_,\
    _delete_product_image_


product = Product.objects.all()


class ProductView:

    def index(self):
        """Загружает главную страницу , с блоками :недавно добавления """

        return render(self, 'TikTak/index.html', {
            'cart_items': Cart.get_items_count(self=self),
            'recently_added_Product': Product.get_recently_added_products(Product(), 4),  # check how it's work
            'users': User,
            'Liked_goods_count': len(_get_user_liked_products_(self)),
            'page_obj': _get_product_pagination_(self, 'liked_product'),
            'Categorys': Product.P_Categorys
        })

    def favorite(self):
        return render(self, 'TikTak/Favorite.html', {
            'Like_product': _get_user_liked_products_(self),
            'Liked_goods_count': len(_get_user_liked_products_(self)),
            'cart_items': Cart.get_items_count(self=self),
        })

    def shop_single_view(self, pk):
        """Загружает страницу с информацией конкретного товара , выбранного по идентификатору(pk-это id товара , переданный по url запросу )"""
        product = Product.objects.get(id=pk)
        return render(self, 'TikTak/shop-single.html', {
            'cart_items': Cart.get_items_count(self=self),
            'product': product,
            'Liked_goods_count': len(_get_user_liked_products_(self)),
            'size_list': product.Product_size
        })

    def shop_view(self):
        """Загружает страницу со всеми товарами , и фильтрует товары , при передаче параметров , по url запросу """
        product = Product.objects.all()

        if self.GET:
            search_input = self.GET.get('Shop_search_input')
            filter_attributes = self.GET.getlist('orderby')
            brand_to_sorted = self.GET.getlist('manufacture_to_sorted')
            gender_to_sort = self.GET.get('gender_orderby')
            sort_size_list = self.GET.getlist('size_to_sort')
            sort_ascending_and_descending = self.GET.get('sort_ascending_and_descending')

            product = _get_filtered_products_(filter_attributes, brand_to_sorted, gender_to_sort,
                                              sort_ascending_and_descending, sort_size_list, search_input)

        return render(self, 'TikTak/shop.html', {
            'cart_items': Cart.get_items_count(self=self),
            'product': product,
            'page_obj': _get_product_pagination_(self, 'product'),
            'Categorys': Product.P_Categorys,
            'Liked_goods_count': len(_get_user_liked_products_(self)),
            'Manufactures': _get_a_product_list_without_dublicate('Product_brand'),
            'Size_list': Product.Choises,
        })

    def profile(self):
        """Загружает страницу , со следующей информацией : Информация о пользователе, сколько товаров пользователь добавил, адррес, эл-почта"""
        return render(self, 'TikTak/Profile.html', {
            'Like_product': _get_user_liked_products_(self),
            'Liked_goods_count': len(_get_user_liked_products_(self)),
            'cart_items': Cart.get_items_count(self=self),
        })

    @login_required
    def add_new_product(self):
        """Загружает страницу добавления товара"""
        return _add_new_product_(self)

    @csrf_exempt
    def DeleteProduct(self):
        id = self.GET.get('Product_id')
        return _delete_product_(user=self.user, Id=id)

    @csrf_exempt
    def EditingProduct(self, Product_id):
        ProductById = Product.objects.get(id=Product_id)
        ProductImagesByProduct = ImageGallery.objects.filter(product=ProductById).order_by('-added_at')
        if self.POST:

            ProductById.Product_name = self.POST.get('changed_product_name')
            ProductById.Product_price = self.POST.get('Product_price')
            ProductById.Product_color = self.POST.get('Product_color')
            ProductById.Product_brand = self.POST.get('Product_brand')
            ProductById.Product_characteristics = self.POST.get('Product_characteristics')
            ProductById.for_which_gender = self.POST.get('changed_for_which_gender')

            ProductById.save()
            return render(self, 'TikTak/ProductEditingView.html', {'product': ProductById, 'ProductImages': ProductImagesByProduct})
        return render(self, 'TikTak/ProductEditingView.html', {'product': ProductById, 'ProductImages': ProductImagesByProduct})

    @csrf_exempt
    def EditingProduct_ajax(self):
        return _editing_product_(self)

    @csrf_exempt
    def addNewProductImage(self):
        return _add_product_image_(self)

    @csrf_exempt
    def ChangeProductImage(self):
        return _change_product_image_(self)


    @csrf_exempt
    def _delete_product_image_(self):
        return _delete_product_image_(self)

'''##################################### SignIn|SignUp section start ##################################'''


class RegAndLoginView:

    def register_view(self):
        """Проверяет данные пользователя из формы , и в случае , если такой пользователь не найден
           регистрирует нового , в ином случае , выполняет вход """
        return _registration_user_(self)

    def login_view(self):
        """Выполняет вход и перенаправляет на главную страницу сайта , в случае , если введенные данные не были найденные в БД
           происходит редирект на форму регистрации"""
        return _login_user_(self)
