from django import forms

from .models import Product, ImageGallery


class LoginForm(forms.Form):
    UserName = forms.CharField(label='Your name', max_length=100)
    Password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'validate-input'}))


class RegisterForm(forms.Form):
    FirstName = forms.CharField(max_length=140)
    LastName = forms.CharField(max_length=140)
    UserName = forms.CharField(label='Your name', max_length=100)
    Email = forms.EmailField(label='Your Email')
    Password = forms.CharField(widget=forms.PasswordInput())
    ConfirmPass = forms.CharField(widget=forms.PasswordInput())


class AddNewProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('Product_name',
                  'Product_price',
                  'Product_brand',
                  'product_description',
                  'Product_color',
                  'Product_size',
                  'Product_characteristics',
                  'for_which_gender',
                  'Product_Category')


class ImageNewProduct(forms.ModelForm):

    class Meta:
        model = ImageGallery
        fields = ('image', )