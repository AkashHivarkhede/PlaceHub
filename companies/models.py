from django.db import models
from django.conf import settings
# Create your models here.




class CompanyProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_profile"
    )

    company_name = models.CharField(
        max_length=200
    )

    phone_number = models.CharField(max_length=15)

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    country = models.CharField(
        max_length=100,
        default="India"
    )

    pincode = models.CharField(
        max_length=10
    )

    description = models.TextField(
        blank=True
    )


    location = models.CharField(
        max_length=200,
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
            default=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.company_name
