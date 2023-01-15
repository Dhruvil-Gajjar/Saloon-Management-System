from django.shortcuts import render


def dashboard(request):
    return render(request, 'core/dashboard.html', context={})


def sign_in(request):
    return render(request, 'auth/sign_in.html', context={})


def sign_up(request):
    return render(request, 'auth/sign_up.html', context={})
