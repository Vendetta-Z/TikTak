from django import forms


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