from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core import paginator

from .forms import LoginForm, RegisterForm
from .models import Product
from Shop_cart.models import Cart
product = Product.objects.all()


class ProductView:

    def index(self):
        Paginator = paginator.Paginator(product, 9)
        page_number = self.GET.get('page')
        page_obj = Paginator.get_page(page_number)

        return render(self, 'TikTak/index.html', {
            'cart_items': Cart.get_items_count(self=self),
            'recently_added_Product': Product.get_recently_added_products(Product(), 4),  # check how it's work
            'users': User,
            'page_obj': page_obj,
            'Categorys': Product.P_Categorys
        })

    def shop_single_view(self, pk):
        product = Product.objects.get(ID_Product=pk)
        return render(self, 'TikTak/shop-single.html', {
            'cart_items': Cart.get_items_count(self=self),
            'product': product,
            'size_list': product.Product_size
        })

    def shop_view(self):
        product = Product.objects.all()

        if self.GET:

            attributes_names = {}
            search_input = self.GET.get('Shop_search_input')
            filter_attributes = self.GET.getlist('orderby')
            brand_to_sorted = self.GET.getlist('manufacture_to_sorted')
            gender_to_sort = self.GET.get('gender_orderby')
            size_to_sort = self.GET.getlist('size_to_sort')
            sort_ascending_and_descending = self.GET.get('sort_ascending_and_descending')

            if filter_attributes:
                attributes_names.update({'Product_Category__in': filter_attributes})
            if brand_to_sorted:
                attributes_names.update({'Product_brand__in': brand_to_sorted})
            if gender_to_sort:
                attributes_names.update({'for_which_gender': gender_to_sort})

            product = Product.objects.filter(**attributes_names)
            
            if sort_ascending_and_descending != '...':
                product = Product.objects.filter(**attributes_names).order_by(sort_ascending_and_descending)

            if size_to_sort:
                size_sort_list = [k for k in product if k.Product_size[0] in size_to_sort or k.Product_size[1] in size_to_sort]
                product = size_sort_list

            if search_input:
                product = product.filter(Product_name__icontains=search_input)

        Paginator = paginator.Paginator(product, 20)
        page_number = self.GET.get('page')
        page_obj = Paginator.get_page(page_number)

        return render(self, 'TikTak/shop.html', {
            'cart_items': Cart.get_items_count(self=self),
            'product': product,
            'page_obj': page_obj,
            'Categorys': Product.P_Categorys,
            'Manufactures': Product.get_a_list_without_dublicate(Product(), 'Product_brand'),
            'Size_list': Product.Choises,
        })


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
