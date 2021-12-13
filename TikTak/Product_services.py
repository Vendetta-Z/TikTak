from django.core import paginator

from .models import Product
from Like.models import Like


product = Product.objects.all()


def _get_user_liked_products_(request):
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
