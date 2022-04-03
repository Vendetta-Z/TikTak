from django.urls import path

from .views import _get_response_to_ajax_request_, _get_Googlenews_api_response

urlpatterns = [
    path('get_news', _get_Googlenews_api_response, name='Get_news'),
    path('get_news_by_number', _get_response_to_ajax_request_, name='get_page_by_number'),
]
