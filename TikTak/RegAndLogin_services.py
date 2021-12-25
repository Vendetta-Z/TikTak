from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm


def _registration_user_(request):
    message = ''
    form = RegisterForm
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid() is not True:
            name = form.cleaned_data['UserName']
            email = form.cleaned_data['Email']
            password = form.cleaned_data['Password']
            ConfirmPass = form.cleaned_data['ConfirmPass']
            if password == ConfirmPass:
                if User.objects.filter(username=name):
                    error = "Такой логин уже существует"
                    return render(request, 'TikTak/register.html',
                                  {'error': error, "message": message, "form": form})
                else:
                    user = User.objects.create_user(name, email, password)
                    login(request, user)
                    return redirect('index')
            else:
                error = 'Пароли не совпадают'
                return render(request, 'TikTak/register.html',
                              {
                                  "error": error,
                                  "message": message,
                                  "form": form
                              })
    return render(request, 'TikTak/register.html', {"form": form, "message": message})


def _login_user_(request):
    message = ''
    form = LoginForm
    if request.method == "GET":
        form = LoginForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['UserName']
            password = form.cleaned_data['Password']
            if authenticate(username=name, password=password):
                user = authenticate(username=name, password=password)
                login(request, user)

                return redirect('index')
            else:
                message = 'проверьте введенные данные!'
                return render(request, 'TikTak/login.html', {'message': message})
        else:
            error = 'Пожалуйста проверьте правильность заполнения формы!. Форма чувствительна к регистру'
            return render(request, 'TikTak/login.html', {"form": form, "message": message, 'error': error})
    else:
        return render(request, 'TikTak/login.html', {'form': form})
