from django.core import paginator
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect


import json

from .forms import AddNewProductForm, ImageNewProduct
from .models import Product, ImageGallery
from Like.models import Like


product = Product.objects.all()


def _get_user_liked_products_(request):
    if request.user.is_anonymous:
        return '0'
    product_liked_user = ''
    product_liked_user = Like.objects.filter(user=request.user)
    liked_products = []
    for id_in_product_liked_users in product_liked_user:
        liked_products.append(Product.objects.get(id=id_in_product_liked_users.object_id))
    return liked_products


def _get_filtered_products_(filter_attributes, brand_to_sorted, gender_to_sort, sort_ascending_and_descending, sort_size_list, search_input):

    attributes_names = {}

    if filter_attributes:
        attributes_names.update({'Product_Category__in': filter_attributes})
    if brand_to_sorted:
        attributes_names.update({'Product_brand__in': brand_to_sorted})
    if gender_to_sort:
        attributes_names.update({'for_which_gender': gender_to_sort})

    product_list = Product.objects.filter(**attributes_names)

    if sort_ascending_and_descending != '...':
        product_list = Product.objects.filter(**attributes_names).order_by(sort_ascending_and_descending)

    if sort_size_list:
        sorted_list_by_size = []
        for product in product_list:
            for size in product.Product_size:
                if size in sort_size_list:
                    sorted_list_by_size.append(product)
        product_list = list(set(sorted_list_by_size))

    if search_input:
        product_list = product_list.filter(Product_name__icontains=search_input)

    return product_list


def _get_product_pagination_(request, query):
    if query == 'liked_product':
        Paginator = paginator.Paginator(Product.objects.order_by('likes'), 9)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(page_number)
        return page_obj
    if query == 'product':
        Paginator = paginator.Paginator(product, 20)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(page_number)
        return page_obj


def _get_a_product_list_without_dublicate(property_name_from_the_list: str):
    """Возвращает список всех товаров , отсортированных по указанному аттрибуту property_name_from_the_list"""
    return Product.get_a_list_without_dublicate(Product(), property_name_from_the_list)


def obj_dict(obj):
    return obj.__dict__


def _add_new_product_(self):
    ImageFormSet = modelformset_factory(ImageGallery,
                                        form=ImageNewProduct, fields=('image',), extra=4)
    ProductList = Product.objects.all()
    if self.POST:
        ProductForm = AddNewProductForm(self.POST)
        formset = ImageFormSet(self.POST, self.FILES, queryset=ImageGallery.objects.none())
        if ProductForm.is_valid() and formset.is_valid():
            Product_Form = ProductForm.save(commit=False)
            Product_Form.save()

            for form in formset.cleaned_data:

                # this helps to not crash if the user
                # do not upload all the photos
                if form:
                    image = form['image']
                    photo = ImageGallery(product=Product_Form, image=image)
                    photo.save()
                # use django messages framework
            messages.success(self, "Yeeew, check it out on the home page!")
            return HttpResponseRedirect("/add_new_product/")
        else:
            print(ProductForm.errors, ImageFormSet.errors)
    else:
        ProductForm = AddNewProductForm()
        formset = ImageFormSet(queryset=ImageGallery.objects.none())

    return render(self, 'TikTak/add_new_product.html',
                  {'postForm': ProductForm,
                   'ProductList': ProductList,
                   'formset': ImageFormSet(queryset=ImageGallery.objects.none())})

@csrf_exempt
def _delete_product_(user, Id):
    Product.objects.get(id=Id).delete()

    all_product_image_list = {}
    for Product_img in Product.objects.all():
        all_product_image_list.update(
            {Product_img.id: Product.objects.get(id=Product_img.id).get_first_image()})

    data = {
        'ProductList': serializers.serialize('json', Product.objects.all()),
        'ProductImages': json.dumps(all_product_image_list, default=obj_dict),
    }
    print(data)
    return JsonResponse(data, safe=False)
