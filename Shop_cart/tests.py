from django.test import TestCase
from django.urls import reverse


class UrlTests(TestCase):

    def test_cart_homepage(self):
        response = self.client.post(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)
