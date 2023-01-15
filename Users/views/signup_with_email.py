from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from Users.utils import generate_otp
from Users.models import Users, EmailOtp
from Users.forms import RegisterEmailForm
from Users.tasks import send_email_verification_otp


@transaction.atomic
def sign_up_with_email(request):
    if request.method == 'POST':
        form = RegisterEmailForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            to_email = form.cleaned_data.get('email')
            mail_subject = 'Activate your account.'
            otp = generate_otp()
            message = render_to_string('auth/send_otp.html', {
                'user': user,
                'otp': otp,
            })

            email_otp_obj, email_otp_obj_created = EmailOtp.objects.get_or_create(email=to_email)
            email_otp_obj.otp = otp
            email_otp_obj.save()

            send_email_verification_otp.delay(mail_subject, message, to_email)
            return redirect('verify-email', e_mail=to_email)
    else:
        form = RegisterEmailForm()

    return render(request, 'auth/sign_up_email.html', context={'form': form})


@transaction.atomic
def verify_email(request, e_mail):
    if request.method == "POST":
        otp = request.POST.get("otp", None)
        email_otp_obj = EmailOtp.objects.filter(email=e_mail, otp=int(otp))
        if otp and email_otp_obj.exists():
            user_obj = Users.objects.filter(email=e_mail).first()
            user_obj.is_active = True
            user_obj.is_customer = True
            user_obj.save()

            email_otp_obj.delete()
            return render(request, 'index.html', context={})
        else:
            messages.error(request, 'Otp entered is not correct !!')
    return render(request, 'auth/verify_otp.html', context={"username": e_mail[-13:]})
