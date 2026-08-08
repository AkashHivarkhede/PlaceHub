import random

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import PasswordResetOTP



def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:

            user = User.objects.get(email=email)

        except User.DoesNotExist:

            messages.error(
                request,
                "No account found with this email."
            )

            return redirect("forgot_password")

        PasswordResetOTP.objects.filter(
            user=user
        ).delete()

        otp = str(random.randint(100000, 999999))

        PasswordResetOTP.objects.create(
            user=user,
            otp=otp
        )

        send_mail(
            subject="Password Reset OTP",
            message=f"Your OTP is {otp}. It is valid for 5 minutes.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        request.session["reset_email"] = email

        messages.success(
            request,
            "OTP sent successfully."
        )

        return redirect("verify_otp")

    return render(
        request,
        "forgot_password.html"
    )


def verify_otp(request):

    email = request.session.get("reset_email")

    if not email:

        return redirect("forgot_password")

    if request.method == "POST":

        otp = request.POST.get("otp")

        user = User.objects.get(email=email)

        try:

            record = PasswordResetOTP.objects.get(
                user=user,
                otp=otp
            )

        except PasswordResetOTP.DoesNotExist:

            messages.error(
                request,
                "Invalid OTP."
            )

            return redirect("verify_otp")

        if record.is_expired():

            record.delete()

            messages.error(
                request,
                "OTP has expired."
            )

            return redirect("forgot_password")

        record.is_verified = True
        record.save()

        return redirect("reset_password")

    return render(
        request,
        "verify_otp.html"
    )



def reset_password(request):

    email = request.session.get("reset_email")

    if not email:

        return redirect("forgot_password")

    user = User.objects.get(email=email)

    try:

        otp = PasswordResetOTP.objects.get(
            user=user,
            is_verified=True
        )

    except PasswordResetOTP.DoesNotExist:

        return redirect("forgot_password")

    if request.method == "POST":

        password = request.POST.get("password")

        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("reset_password")

        user.password = make_password(password)

        user.save()

        otp.delete()

        request.session.flush()

        messages.success(
            request,
            "Password changed successfully."
        )

        return redirect("login")

    return render(
        request,
        "reset_password.html"
    )


def resend_otp(request):

    email = request.session.get("reset_email")

    if not email:

        return redirect("forgot_password")

    user = User.objects.get(email=email)

    PasswordResetOTP.objects.filter(
        user=user
    ).delete()

    otp = str(random.randint(100000, 999999))

    PasswordResetOTP.objects.create(
        user=user,
        otp=otp
    )

    send_mail(
        subject="Password Reset OTP",
        message=f"Your new OTP is {otp}.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

    messages.success(
        request,
        "New OTP sent."
    )

    return redirect("verify_otp")



from django.contrib.auth.hashers import make_password
from django.contrib import messages

def reset_password(request):

    email = request.session.get("reset_email")

    if not email:
        return redirect("forgot_password")

    user = User.objects.get(email=email)

    try:
        otp = PasswordResetOTP.objects.get(
            user=user,
            is_verified=True
        )

    except PasswordResetOTP.DoesNotExist:
        messages.error(request, "OTP verification required.")
        return redirect("forgot_password")

    if otp.is_expired():
        otp.delete()
        messages.error(request, "OTP has expired.")
        return redirect("forgot_password")

    if request.method == "POST":

        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password")

        if len(password) < 8:
            messages.error(
                request,
                "Password must contain at least 8 characters."
            )
            return redirect("reset_password")

        user.password = make_password(password)
        user.save()

        otp.delete()

        request.session.pop("reset_email", None)

        messages.success(
            request,
            "Password changed successfully."
        )

        return redirect("login")

    return render(request, "reset_password.html")