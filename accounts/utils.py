import random

from django.conf import settings
from django.core.mail import send_mail

from .models import EmailVerificationOTP


def send_verification_otp(user):

    otp = str(
        random.randint(100000, 999999)
    )

    EmailVerificationOTP.objects.update_or_create(
        user=user,
        defaults={
            "otp": otp
        }
    )

    send_mail(
        subject="Verify Your PlaceHub Email",

        message=f"""
Hello {user.username},

Welcome to PlaceHub!

Your email verification OTP is:

{otp}

This OTP is valid for 10 minutes.

Please do not share this OTP with anyone.

Regards,
PlaceHub Team
""",

        from_email=settings.EMAIL_HOST_USER,

        recipient_list=[
            user.email
        ],

        fail_silently=False
    )