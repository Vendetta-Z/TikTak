from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as dj_login
from django.core import paginator

from .forms import LoginForm, RegisterForm
from .models import Product
from .Cart import Cart

product = Product.objects.all()





class ProductView():

    def index(request):
        Paginator = paginator.Paginator(product, 9)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(page_number)

        #Product.CreateProduct('self')
        return render(request, 'TikTak/index.html', {'product': product, 'users': User, 'page_obj': page_obj, 'Categorys':Product.P_Categorys})

    def view_category(request, key):
        answer_category = key.replace(' ', '')
        product = Product.objects.filter(Product_Category=answer_category)
        Paginator = paginator.Paginator(product, 9)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(page_number)
        return render(request, 'TikTak/index.html', {'product': product, 'users': User, 'page_obj': page_obj, 'Categorys': Product.P_Categorys} )

    def Shop_single_view(request, pk):
        product = Product.objects.get(ID_Product=pk)
        return render(request, 'TikTak/shop-single.html', {'product': product, 'size_list': product.Product_size})

    def Shop_view(request):
        product = Product.objects.all()

        if request.GET:
            attributes_names = {}
            search_input = request.GET.get('Shop_search_input')
            filter_attributes = request.GET.getlist('orderby')
            brand_to_sorted = request.GET.getlist('manufacture_to_sorted')
            gender_to_sort = request.GET.get('gender_orderby')
            size_to_sort = request.GET.getlist('size_to_sort')

            if filter_attributes:
                attributes_names.update({'Product_Category__in': filter_attributes})
            if brand_to_sorted:
                attributes_names.update({'Product_brand__in': brand_to_sorted})
            if gender_to_sort:
                attributes_names.update({'for_which_gender': gender_to_sort})



            product = Product.objects.filter(**attributes_names)

            if size_to_sort:
                size_sort_list = [k for k in product if k.Product_size[0] in size_to_sort or k.Product_size[1] in size_to_sort]
                product = size_sort_list



            if search_input:
                product = product.filter(Product_name__icontains=search_input)





        Paginator = paginator.Paginator(product, 20)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(page_number)

        return render(request, 'TikTak/shop.html', {
                                                    'product': product,
                                                    'page_obj': page_obj,
                                                    'Categorys': Product.P_Categorys,
                                                    'Manufactures': Product.get_a_list_without_dublicate('self','Product_brand'),
                                                    'Size_list': Product.Choises,
        })


    def Shop_view_Category(request, key):
        answer_category = key.replace(' ', '')
        if key == 'All_products':
            product = Product.objects.all()
        Paginator = paginator.Paginator(product, 20)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(page_number)
        return redirect('Shop')


class RegAndLoginView():

    def RegisterView(request):
        error = ''
        message = ''
        form = RegisterForm
        if request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid() is not True:
                name = form.cleaned_data['UserName']
                email = form.cleaned_data['Email']
                password = form.cleaned_data['Password']
                ConfirmPass = form.cleaned_data['ConfirmPass']
                if password == ConfirmPass:
                    if User.objects.filter(username=name):
                        error = "Такой логин уже существует"
                        return render(request, 'TikTak/register.html', {'error': error, "message": message, "form": form})
                    else:
                        user = User.objects.create_user(name, email, password)
                        dj_login(request, user)
                        return redirect('index')
                else:
                    error = 'Пароли не совпадают'
                    return render(request, 'TikTak/register.html', {'error': error, "message": message, "form": form})


            else:
                error = "Error fuck'er mother fuck'er"

        return render(request, 'TikTak/register.html', {"form": form, "message": message})


    def LoginView(request):
        message = ''
        form = LoginForm
        if request.method == "GET":
            form = LoginForm(request.GET)
            if form.is_valid():
                name = form.cleaned_data['UserName']
                password = form.cleaned_data['Password']
                if authenticate(username=name, password=password):
                    user = authenticate(username=name, password=password)
                    login(request, user)

                    return redirect('index')
                else:
                    message = 'проверьте введенные данные!'
                    return render(request, 'TikTak/login.html', {'message': message})
            else:
                error = 'Пожалуйста проверьте правильность заполнения формы!. Форма чувствительна к регистру'
                return render(request, 'TikTak/login.html', {"form": form, "message": message})
        else:
            return render(request, 'TikTak/login.html', {'form': form})


'''##################################### Cart section start ##################################'''
class Shop_сart():
    @login_required(login_url="/users/login")
    def cart_add(request, ID_Product):
        cart = Cart(request)
        quantity = request.POST.get('quantity')
        size = request.POST.get('size')

        product = Product.objects.get(ID_Product=ID_Product)
        cart.add(product=product, quantity=quantity, size=size, color='black')
        cart.save()
        return redirect("index")


    @login_required(login_url="/users/login")
    def item_clear(request, ID_Product):
        cart = Cart(request)
        product = Product.objects.get(ID_Product=ID_Product)
        cart.remove(product)
        return redirect("cart_detail")


    @login_required(login_url="/users/login")
    def item_increment(request, key):
        cart = Cart(request)
        cart.increment(key=key)
        return redirect("cart_detail")

    @login_required(login_url="/users/login")
    def item_decrement(request, key):
        cart = Cart(request)
        cart.decrement(key=key)
        return redirect("cart_detail")


    @login_required(login_url="/users/login")
    def cart_clear(request):
        cart = Cart(request)
        cart.clear()
        return redirect("cart_detail")


    @login_required(login_url="/users/login")
    def cart_detail(request):
        a = []
        b = []
        cart = Cart(request).cart.items()
        for key, value in  cart:
            a.append(value['quantity'])
            b.append(value['price'])

        quantity = [int(item) for item in a]
        price = [int(item) for item in b]

        total_sum = 0
        for i in range(len(quantity)):
            total_sum += quantity[i] * price[i]

        return render(request, 'cart/detail.html', {'total_sum': total_sum})


    @login_required(login_url='/users/login')
    def item_remove(request, key):
        cart = Cart(request)
        cart.remove(key=key)
        return redirect('cart_detail')