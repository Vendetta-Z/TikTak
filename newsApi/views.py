from django.shortcuts import render
from django.core import paginator
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.forms.models import model_to_dict

import requests
import json

# Create your views here.
url = "https://newsapi.org/v2/top-headlines?q=Phone&apiKey=2dd2335d7d1b444395484ee5ce5ad8b2"
# querystring = {"q": ["Samsung", "Samsung", "Xiaomi", "Iphone"], "lang": "ru"}
#
# headers = {
#     'x-rapidapi-host': "free-news.p.rapidapi.com",
#     'x-rapidapi-key': "7ace2e8d31msh8c224b8e1584644p14cb88jsn80e238ac989f"
# }

response = requests.request("GET", url)

data = response.json()
print(data)
articles = data['articles']
Paginator = paginator.Paginator(articles, 4)


def _get_Googlenews_api_response(request):
    page_number = request.GET.get('NewsPageNumber')
    page_obj = Paginator.get_page(page_number)
    return page_obj


def _get_response_to_ajax_request_(request):

    NewsPageNumber = request.GET.get('NewsPageNumber')
    page_obj = Paginator.get_page(NewsPageNumber)
    page_obj_dict = {}
    print(page_obj.__len__())
    for obj in page_obj:
        print(type(obj.keys()))
        page_obj_dict.update(key, value)

    return JsonResponse(page_obj_dict, safe=False)
