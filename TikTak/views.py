from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

from Like.models import Like
from Shop_cart.models import Cart

from .forms import AddNewProductForm, ImageNewProduct
from .models import Product, ImageGallery
from .RegAndLogin_services import _registration_user_, _login_user_
from .Product_services import _get_a_product_list_without_dublicate, _get_user_liked_products_, _get_filtered_products_, \
    _get_product_pagination_

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
        ImageFormSet = modelformset_factory(ImageGallery,
                                            form=ImageNewProduct, fields=('image',), extra=4)

        if self.POST:
            print('прошла проверку пост запроса ')
            ProductForm = AddNewProductForm(self.POST)
            formset = ImageFormSet(self.POST, self.FILES, queryset=ImageGallery.objects.none())
            print(formset)
            if ProductForm.is_valid() and formset.is_valid():
                print('прошла проверку валидности ')
                Product_Form = ProductForm.save(commit=False)
                Product_Form.save()

                for form in formset.cleaned_data:
                    print('Проходит цикл клин дата ')

                    # this helps to not crash if the user
                    # do not upload all the photos
                    if form:
                        image = form['image']
                        photo = ImageGallery(product=Product_Form, image=image)
                        photo.save()
                    # use django messages framework
                messages.success(self, "Yeeew, check it out on the home page!")
                return HttpResponseRedirect("/")
            else:
                print('запрос не прошел проверку валидности')
                print(ProductForm.errors, ImageFormSet.errors)
        else:
            ProductForm = AddNewProductForm()
            formset = ImageFormSet(queryset=ImageGallery.objects.none())

        print('fuck')
        return render(self, 'TikTak/add_new_product.html',
                      {'postForm': ProductForm, 'formset': ImageFormSet(queryset=ImageGallery.objects.none())})


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
