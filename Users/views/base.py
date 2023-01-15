import re

from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import AuthenticationForm

from Users.models import Users


def dashboard(request):
    return render(request, 'core/dashboard.html', context={})


def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        if re.search(r'^[6-9]\d{9}$', username):
            user_obj = Users.objects.filter(Q(phone_number=username) | Q(username=username))
            if user_obj.exists():
                if user_obj.first().is_active:
                    if user_obj.first().check_password(password):
                        login(request, user_obj.first(), backend='django.contrib.auth.backends.ModelBackend')
                        return redirect(reverse('dashboard'))
                    else:
                        messages.error(request, 'Phone number or password not correct !!')
                        return redirect(reverse('sign-in'))
                else:
                    messages.error(request, 'Please activate your account !!')
                    return redirect(reverse('sign-in'))
            else:
                messages.error(request, 'Account with this Phone number does not exist !!')
                return redirect(reverse('sign-in'))
        else:
            user_obj = Users.objects.filter(Q(email=username) | Q(username=username))
            if user_obj.exists():
                if user_obj.first().is_active:
                    if user_obj.first().check_password(password):
                        login(request, user_obj.first(), backend='django.contrib.auth.backends.ModelBackend')
                        return redirect(reverse('dashboard'))
                    else:
                        messages.error(request, 'Email or password not correct !!')
                        return redirect(reverse('sign-in'))
                else:
                    messages.error(request, 'Please activate your account !!')
                    return redirect(reverse('sign-in'))
            else:
                messages.error(request, 'Account with this email does not exist !!')
                return redirect(reverse('sign-in'))
    else:
        form = AuthenticationForm()

    # return render(request, 'Auth/login-new.html', {'form': form})
    return render(request, 'auth/sign_in.html', context={'form': form})


def sign_up(request):
    return render(request, 'auth/sign_up.html', context={})
