from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core import paginator
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
import json
from django.core import serializers

from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm, RegisterForm
from .models import Product, Like
from Shop_cart.models import Cart

product = Product.objects.all()


class ProductView:

    def index(self):
        Paginator = paginator.Paginator(Product.objects.order_by('likes'), 9)
        page_number = self.GET.get('page')
        page_obj = Paginator.get_page(page_number)

        id_of_liked_goods = Like.objects.filter(user=self.user)
        liked_product = []
        for i in id_of_liked_goods:
            liked_product.append(Product.objects.get(id=i.object_id))

        return render(self, 'TikTak/index.html', {
            'cart_items': Cart.get_items_count(self=self),
            'recently_added_Product': Product.get_recently_added_products(Product(), 4),  # check how it's work
            'users': User,
            'Liked_goods_count': len(liked_product),
            'page_obj': page_obj,
            'Categorys': Product.P_Categorys
        })

    def shop_single_view(self, pk):

        id_of_liked_goods = Like.objects.filter(user=self.user)
        liked_product = []
        for i in id_of_liked_goods:
            liked_product.append(Product.objects.get(id=i.object_id))

        product = Product.objects.get(id=pk)
        return render(self, 'TikTak/shop-single.html', {
            'cart_items': Cart.get_items_count(self=self),
            'product': product,
            'Liked_goods_count': len(liked_product),
            'size_list': product.Product_size
        })

    def shop_view(self):

        id_of_liked_goods = Like.objects.filter(user=self.user)
        liked_product = []
        for i in id_of_liked_goods:
            liked_product.append(Product.objects.get(id=i.object_id))

        product = Product.objects.all()

        if self.GET:

            attributes_names = {}
            search_input = self.GET.get('Shop_search_input')
            filter_attributes = self.GET.getlist('orderby')
            brand_to_sorted = self.GET.getlist('manufacture_to_sorted')
            gender_to_sort = self.GET.get('gender_orderby')
            sort_size_list = self.GET.getlist('size_to_sort')
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

            if sort_size_list:
                sorted_list_by_size = []
                for P in product:
                    for size in P.Product_size:
                        if size in sort_size_list:
                            sorted_list_by_size.append(P)
                product = list(set(sorted_list_by_size))

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
            'Liked_goods_count': len(liked_product),
            'Manufactures': Product.get_a_list_without_dublicate(Product(), 'Product_brand'),
            'Size_list': Product.Choises,
        })

    def Profile(self):
        id_of_liked_goods = Like.objects.filter(user=self.user)
        liked_product = []
        for i in id_of_liked_goods:
            liked_product.append(Product.objects.get(id=i.object_id))

        return render(self, 'TikTak/Profile.html', {
            'Like_product': liked_product,
            'Liked_goods_count': len(liked_product),
            'cart_items': Cart.get_items_count(self=self),
        })


class DynamicProductView(View):
    @csrf_exempt
    def add_like(self, *args, **kwargs):
        pk = self.GET.get('Product_id')
        Data_code = self.GET.get('DLP')

        like_product = Product.objects.get(id=pk)
        Product_type = ContentType.objects.get_for_model(like_product)
        Like.objects.create(content_type=Product_type, object_id=like_product.id, user=self.user)
        Likes_count = Like.objects.filter(user=self.user, object_id=pk)
        if len(Likes_count) > 1:
            ''''GET /add_like?Product_id=12&DLP=1 HTTP/1.1" 200 865 '''
            ''' GET /add_like?Product_id=12&DLP=1 HTTP/1.1" 200 865 '''
            if Data_code == '1':
                Like.objects.filter(user=self.user, object_id=pk).delete()
                all_products_liked_by_the_user = []
                liked_products = Like.objects.filter(user=self.user)
                main_first_picture_of_product = {}

                def obj_dict(obj):
                    return obj.__dict__

                for l_product in liked_products:
                    main_first_picture_of_product.update({l_product.object_id: Product.objects.get(id=l_product.object_id).get_first_image()})
                    all_products_liked_by_the_user += [Product.objects.get(id=l_product.object_id)]

                data = {
                    'one': 'Product successful unliked',
                    'Like_product_pictures': json.dumps(main_first_picture_of_product, default=obj_dict),
                    'Like_product': (serializers.serialize('json', all_products_liked_by_the_user)),
                    'Like_p_len': len(Like.objects.filter(object_id=pk, user=self.user))}
                return JsonResponse(data, safe=False)

            Like.objects.filter(user=self.user, object_id=pk).delete()
            data = {
                'one': 'Product successful unliked',
                'two': len(Like.objects.filter(object_id=pk, user=self.user))}
            return JsonResponse(data, safe=False)
        else:
            data = {
                'one': [(serializers.serialize('json', (Product.get_recently_added_products(Product(), 4))))],
                'two': len(Like.objects.filter(object_id=pk, user=self.user))}
            return JsonResponse(data, safe=False)

    def is_liked(self):
        Product_id = self.GET.get('Product_id')
        likes_count = Like.objects.filter(object_id=Product_id, user=self.user)

        if len(likes_count) > 0:
            return JsonResponse({'is_liked': 'True'}, safe=False)
        else:
            return JsonResponse({'is_liked': 'False'}, safe=False)
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
