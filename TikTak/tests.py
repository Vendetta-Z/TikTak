from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
# Create your tests here.


class UrlTests(TestCase):

    def test_homepage(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_shop(self):
        responce = self.client.get("/Shop/")
        self.assertEqual(responce.status_code, 200)

    # --------------------- Testing signIn and signUp Url ----------------------

    def setUp(self):
        self.username = 'testuser'
        self.email = 'example@gmail.com'
        self.password = 'secret'
        self.password2 = 'secret'
        User.objects.create_user(self.username, self.password)

    def test_login(self):
        response = self.client.post('/login/', self.username, self.password, follow=True)
        self.assertTrue(User.is_authenticated)

    def test_signUp(self):
        response = self.client.post(reverse('register'), data={
            'UserName': self.username,
            'Email': self.email,
            'Password': self.password,
            'ConfirmPass': self.password2})
        self.assertEqual(response.status_code, 200)
