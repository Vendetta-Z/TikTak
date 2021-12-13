from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

from .forms import LoginForm, RegisterForm
from Like.models import Like
from .models import Product
from Shop_cart.models import Cart
from .Product_services import _get_product_pagination_, _get_user_liked_products_, _get_filtered_products_

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

        product = Product.objects.get(id=pk)
        return render(self, 'TikTak/shop-single.html', {
            'cart_items': Cart.get_items_count(self=self),
            'product': product,
            'Liked_goods_count': len(_get_user_liked_products_(self)),
            'size_list': product.Product_size
        })

    def shop_view(self):

        product = Product.objects.all()

        if self.GET:

            search_input = self.GET.get('Shop_search_input')
            filter_attributes = self.GET.getlist('orderby')
            brand_to_sorted = self.GET.getlist('manufacture_to_sorted')
            gender_to_sort = self.GET.get('gender_orderby')
            sort_size_list = self.GET.getlist('size_to_sort')
            sort_ascending_and_descending = self.GET.get('sort_ascending_and_descending')

            product = _get_filtered_products_(filter_attributes, brand_to_sorted, gender_to_sort, sort_ascending_and_descending, sort_size_list, search_input)

        return render(self, 'TikTak/shop.html', {
            'cart_items': Cart.get_items_count(self=self),
            'product': product,
            'page_obj': _get_product_pagination_(self, 'product'),
            'Categorys': Product.P_Categorys,
            'Liked_goods_count': len(_get_user_liked_products_(self)),
            'Manufactures': Product.get_a_list_without_dublicate(Product(), 'Product_brand'),
            'Size_list': Product.Choises,
        })

    def profile(self):

        return render(self, 'TikTak/Profile.html', {
            'Like_product': _get_user_liked_products_(self),
            'Liked_goods_count': len(_get_user_liked_products_(self)),
            'cart_items': Cart.get_items_count(self=self),
        })

    def add_new_product(self):
        template_name = 'TikTak/add_new_product.html'
        return render(self, template_name)

'''##################################### SignIn|SignUp section start ##################################'''


class RegAndLoginView:

    def register_view(self):
        message = ''
        form = RegisterForm
        if self.POST:
            form = RegisterForm(self.POST)
            if form.is_valid() is not True:
                name = form.cleaned_data['UserName']
                email = form.cleaned_data['Email']
                password = form.cleaned_data['Password']
                ConfirmPass = form.cleaned_data['ConfirmPass']
                if password == ConfirmPass:
                    if User.objects.filter(username=name):
                        error = "Такой логин уже существует"
                        return render(self, 'TikTak/register.html',
                                      {'error': error, "message": message, "form": form})
                    else:
                        user = User.objects.create_user(name, email, password)
                        login(self, user)
                        return redirect('index')
                else:
                    error = 'Пароли не совпадают'
                    return render(self, 'TikTak/register.html',
                                  {
                                      "error": error,
                                      "message": message,
                                      "form": form
                                  })

        return render(self, 'TikTak/register.html', {"form": form, "message": message})

    def login_view(self):
        message = ''
        form = LoginForm
        if self.method == "GET":
            form = LoginForm(self.GET)
            if form.is_valid():
                name = form.cleaned_data['UserName']
                password = form.cleaned_data['Password']
                if authenticate(username=name, password=password):
                    user = authenticate(username=name, password=password)
                    login(self, user)

                    return redirect('index')
                else:
                    message = 'проверьте введенные данные!'
                    return render(self, 'TikTak/login.html', {'message': message})
            else:
                error = 'Пожалуйста проверьте правильность заполнения формы!. Форма чувствительна к регистру'
                return render(self, 'TikTak/login.html', {"form": form, "message": message, 'error': error})
        else:
            return render(self, 'TikTak/login.html', {'form': form})
