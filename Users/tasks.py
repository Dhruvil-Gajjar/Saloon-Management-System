from celery import shared_task
from twilio.rest import Client
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection

from Project.celery import app


@app.task()
def send_email_verification_otp(mail_subject, message, to_email):
    try:
        connection = get_connection(fail_silently=False)

        email = EmailMultiAlternatives(
            subject=mail_subject,
            body="Verify E-Mail",
            from_email="dhruvilvi.dev@gmail.com",
            to=[to_email],
            connection=connection
        )
        email.attach_alternative(message, "text/html")
        email.send()

        print('#### >>>>>>>>>>>>>>>>>>>>>>>> Email has been sent successfully to %s !!' % to_email)
    except Exception as err:
        print('#### >>>>>>>>>>>>>>>>>>>>>>>> Error in sending email to %s.' % to_email)
        print(err)


@app.task()
def send_number_verification_otp(to_number, otp):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            to=f"+91{to_number}",
            from_="+16086556226",
            body=f"{otp} is your OTP for signing up to Saloon. Never share OTP.",
        )
        print('#### >>>>>>>>>>>>>>>>>>>>>>>> Otp has been sent successfully to %s !!' % to_number)
    except Exception as err:
        print('#### >>>>>>>>>>>>>>>>>>>>>>>> Error in sending otp to %s.' % to_number)
        print(err)
