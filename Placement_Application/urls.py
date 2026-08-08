from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("accounts.urls")),
    path("", include('students.urls')),
    # path("", include("companies.urls")),
    path("", include("jobs.urls")),
    path("", include("passwords.urls")),

    
    path("accounts/", include("allauth.urls")),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)