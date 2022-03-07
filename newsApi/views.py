from django.shortcuts import render
from django.core import paginator
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.forms.models import model_to_dict

import requests
import json


# Create your views here.
url = "https://free-news.p.rapidapi.com/v1/search"

querystring = {"q": ["Samsung", "Samsung", "Xiaomi", "Iphone"], "lang": "ru"}

headers = {
    'x-rapidapi-host': "free-news.p.rapidapi.com",
    'x-rapidapi-key': "7ace2e8d31msh8c224b8e1584644p14cb88jsn80e238ac989f"
}

response = requests.request("GET", url, headers=headers, params=querystring)
data = response.json()
articles = data['articles']
Paginator = paginator.Paginator(articles, 4)


def _get_Googlenews_api_response(request):
    page_number = request.GET.get('NewsPageNumber')
    page_obj = Paginator.get_page(page_number)
    return page_obj


def _get_response_to_ajax_request_(request):
    page_obj = Paginator.get_page(request)
    for i in page_obj:
        i = dict(i)
    return HttpResponse(json.dumps(page_obj))
