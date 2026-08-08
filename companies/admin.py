from django.contrib import admin
from .models import CompanyProfile
# Register your models here.

class adminCompany(admin.ModelAdmin):
    list_display = ['user' , 'company_name' , 'phone_number' ,  'state' , 'location' , 'website']


admin.site.register(CompanyProfile , adminCompany)



