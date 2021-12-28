from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
import json

from .models import Like
from TikTak.models import Product


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