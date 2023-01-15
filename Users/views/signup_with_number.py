import pyotp
import base64

from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect

from Users.models import Users
from Users.utils import generateKey
from Users.forms import RegisterNumberForm
from Users.tasks import send_number_verification_otp


@transaction.atomic
def sign_up_with_number(request):
    if request.method == 'POST':
        form = RegisterNumberForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            phone_number = form.cleaned_data.get('phone_number')
            keygen = generateKey()
            key = base64.b32encode(keygen.returnValue(phone_number).encode())  # Key is generated
            OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created

            send_number_verification_otp.delay(phone_number, OTP.at(1))
            return redirect('verify-number', phone_number=phone_number)
    else:
        form = RegisterNumberForm()

    return render(request, 'auth/sign_up_number.html', context={"form": form})


@transaction.atomic
def verify_number(request, phone_number):
    if request.method == "POST":
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone_number).encode())  # Generating Key
        OTP = pyotp.HOTP(key)  # HOTP Model

        if OTP.verify(request.POST.get("otp", None), 1):  # Verifying the OTP
            user_obj = Users.objects.filter(phone_number=phone_number).first()
            user_obj.is_active = True
            user_obj.is_customer = True
            user_obj.save()

            return render(request, 'index.html', context={})
        else:
            messages.error(request, 'Otp entered is not correct !!')

    return render(request, 'auth/verify_otp.html', context={"username": phone_number[-4:]})
