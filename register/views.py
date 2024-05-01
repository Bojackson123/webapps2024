from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.conf import settings
import requests

@csrf_protect
def Login(request):
    if request.method == 'POST':
        login_credential = request.POST.get('login_credential')
        password = request.POST.get('password')

        if not login_credential or not password:
            messages.error(request, 'Both username/email and password are required.')
            return redirect('/webapps2024/login/')

        # Check if the login credential is an email
        if '@' in login_credential:
            user_obj = User.objects.filter(email=login_credential).first()
        else:
            user_obj = User.objects.filter(username=login_credential).first()

        if user_obj is None:
            messages.error(request, 'User not found.')
            return redirect('/webapps2024/login/')

        user = authenticate(username=user_obj.username, password=password)

        if user is None:
            messages.error(request, 'Wrong password.')
            return redirect('/webapps2024/login/')

        login(request, user)
        messages.success(request, 'Welcome, ' + user_obj.username)
        return redirect('/')

    return render(request, 'login.html')


@csrf_protect
def Register(request):
    try:
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            currency = request.POST.get('currency')

        try:
            if User.objects.filter(username = username).first():
                messages.error(request, 'Username is taken.')
                return redirect('/webapps2024/register/')

            if User.objects.filter(email = email).first():
                messages.error(request, 'Email is taken.')
                return redirect('/webapps2024/register/')

            if not request.POST.get('currency') == 'GBP':

                url = request.build_absolute_uri(
                    reverse('convert_currency', kwargs={
                        'currency1': 'GBP', 'currency2': request.POST.get('currency'),
                        'amount_of_currency1': '1000.00'
                    })
                )
                response = requests.get(url, verify=settings.VERIFY_SSL)
                data = response.json()
                converted_balance = float(data["converted_amount"])
                user_obj = User(username = username , email = email, first_name = first_name,
                                last_name = last_name, currency=currency, balance= converted_balance)
                user_obj.set_password(password)
                user_obj.save()
                messages.success(request, 'Account created successfully.')
            else:
                user_obj = User(username = username , email = email, first_name = first_name,
                                last_name = last_name, currency=currency)
                user_obj.set_password(password)
                user_obj.save()
                messages.success(request, 'Account created successfully.')

            return redirect('/webapps2024/login/')

        except Exception as e:
            print(e)

    except Exception as e:
        print(e)

    return render(request, 'register.html')


def Logout(request):
    logout(request)
    return redirect('/')

