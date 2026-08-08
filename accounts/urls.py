from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.login_view, name='login'),

    path('logout' , views.logeout , name='logout'),

    path('signup/student/', views.student_signup, name='signup_student'),

    path('signup/company/', views.company_signup, name='signup_company'),

    path(
    "verify-email/",
    views.verify_email,
    name="verify_email"
),

path(
    "resend-verification-otp/",
    views.resend_verification_otp,
    name="resend_verification_otp"
),
]