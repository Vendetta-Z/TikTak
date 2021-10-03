from django.contrib.auth.forms import UserCreationForm
from django.db import models


class Users(UserCreationForm):
    UserName = models.CharField('username', max_length=150)
    FirstName = models.CharField('FirstName', max_length=120)
    LastName = models.CharField('LastName', max_length=90)
    Password = models.CharField('Password', max_length=120)
    Email = models.EmailField('Email', default='example@gmail.com')

    def __str__(self):
        return self.FirstName