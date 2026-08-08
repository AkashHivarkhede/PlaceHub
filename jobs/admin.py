from django.contrib import admin
from .models import JobApplication , JobRequirement , Qualification
# Register your models here.


class adminQualification(admin.ModelAdmin):
    list_display = ['name']

class adminJobRequirement(admin.ModelAdmin):
    list_display = ['company' , 'job_title' , 'job_code' , 'location' , 'posted_at']

class adminJobApplication(admin.ModelAdmin):
    list_display = ['student' , 'job' , 'applied_at' , 'stage']

admin.site.register(JobRequirement , adminJobRequirement)
admin.site.register(JobApplication , adminJobApplication)
admin.site.register(Qualification , adminQualification)