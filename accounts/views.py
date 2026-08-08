from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
# from django.contrib.auth.decorators import login_required

from students.models import StudentProfile
from students.models import CompanyProfile
from .utils import send_verification_otp
from .models import EmailVerificationOTP

        
def login_view(request):
    if request.method == 'GET':
        return render(request , 'login.html')
    else:
        username = request.POST["username"]
        password = request.POST["password"]

        # Check whether user entered an email

        if "@" in username:
            try:
                user_obj = User.objects.get(email__iexact=username)
                username = user_obj.username
            except User.DoesNotExist:
                return render(request , 'login.html' , {'error' : 'Invalid username/email or password.'})


        user = authenticate(request, username = username , password = password)


        if user is not None:

            if not user.is_active:

                messages.error(
                    request,
                    "Please verify your email before logging in."
                )

                return redirect("login")

            login(request, user)

            return redirect("student_dashboard")

        else:
             return render(
                    request,
                    "login.html",
                    {
                        "error": "Invalid username/email or password."
                    }
                )



def student_signup(request):

    if request.method == "GET":
        return render(request, "student_signup.html")

    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm_password")

    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    phone_number = request.POST.get("phone")

    if password != confirm_password:
        messages.error(request, "Password and Confirm Password do not match")
        return redirect("signup_student")

    if User.objects.filter(username=username).exists():
        messages.error(request, "Username already exists.")
        return redirect("signup_student")

    if User.objects.filter(email=email).exists():
        messages.error(request, "Email already exists.")
        return redirect("signup_student")

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_active=False
    )

    StudentProfile.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number
    )

    # Send verification OTP

    send_verification_otp(user)

    # IMPORTANT
    # Remove password-reset session if it exists
    request.session.pop("reset_email", None)

    request.session["verify_email"] = email

    request.session.modified = True


    messages.success(
        request,
        "Verification OTP has been sent to your email."
    )

    return redirect("verify_email")



def company_signup(request):

    if request.method == "GET":
        return render(request, "company_signup.html")

    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]

    company_name = request.POST["company_name"]
    phone_number = request.POST["phone"]

    if User.objects.filter(username=username).exists():
        messages.error(request, "Username already exists.")
        return redirect("signup_company")

    if User.objects.filter(email=email).exists():
        messages.error(request, "Email already exists.")
        return redirect("signup_company")

    if CompanyProfile.objects.filter(company_name=company_name).exists():
        messages.error(request, "Company already registered.")
        return redirect("signup_company")

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_active=False
    )

    CompanyProfile.objects.create(
        user=user,
        company_name=company_name,
        phone_number=phone_number
    )

    send_verification_otp(user)

    request.session.pop("reset_email", None)

    request.session["verify_email"] = email

    request.session.modified = True


    messages.success(
        request,
        "Verification OTP has been sent to your email."
    )

    return redirect("verify_email")



def verify_email(request):

    email = request.session.get("verify_email")

    if not email:

        messages.error(
            request,
            "Verification session expired. Please register again."
        )

        return redirect("signup_student")

    try:

        user = User.objects.get(
            email__iexact=email
        )

    except User.DoesNotExist:

        messages.error(
            request,
            "User account not found."
        )

        return redirect("signup_student")

    try:

        verification = EmailVerificationOTP.objects.get(
            user=user
        )

    except EmailVerificationOTP.DoesNotExist:

        messages.error(
            request,
            "Verification OTP not found. Please request a new OTP."
        )

        return redirect("verify_email")

    if request.method == "POST":

        if request.method == "POST":

            otp = (
                request.POST.get("otp1", "") +
                request.POST.get("otp2", "") +
                request.POST.get("otp3", "") +
                request.POST.get("otp4", "") +
                request.POST.get("otp5", "") +
                request.POST.get("otp6", "")
                )

            print("OTP ENTERED:", otp)

        entered_otp = request.POST.get(
            "otp",
            ""
        ).strip()

        print("ENTERED OTP:", entered_otp)
        print("DATABASE OTP:", verification.otp)

        if not entered_otp:

            messages.error(
                request,
                "Please enter the OTP."
            )

            return redirect("verify_email")

        if verification.is_expired():

            verification.delete()

            messages.error(
                request,
                "OTP has expired. Please request a new OTP."
            )

            return redirect("verify_email")

        if entered_otp != verification.otp:

            messages.error(
                request,
                "Invalid OTP. Please try again."
            )

            return redirect("verify_email")

        # -------------------------------
        # OTP IS CORRECT
        # -------------------------------

        user.is_active = True
        user.save()

        verification.delete()

        request.session.pop(
            "verify_email",
            None
        )

        messages.success(
            request,
            "Email verified successfully. You can now login."
        )

        return redirect("login")

    return render(
        request,
        "verify_email.html"
    )

def resend_verification_otp(request):

    email = request.session.get("verify_email")

    if not email:

        messages.error(
            request,
            "Verification session expired. Please register again."
        )

        return redirect("signup_student")

    try:

        user = User.objects.get(
            email__iexact=email
        )

    except User.DoesNotExist:

        messages.error(
            request,
            "User account not found."
        )

        return redirect("signup_student")

    send_verification_otp(user)

    messages.success(
        request,
        "New verification OTP has been sent to your email."
    )

    return redirect("verify_email")


def logeout(request):
    request.session.clear()
    return redirect('home')


