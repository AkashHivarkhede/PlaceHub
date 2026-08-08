from django.contrib import admin
from .models import (StudentProfile , Skill , JobPosition , JobLocation , Hobby ,Interest , Education , Project) 


class adminStudent(admin.ModelAdmin):
    list_display = ['user' , 'first_name' , 'last_name' , 'phone_number' , 'created_at' , 'updated_at' ]

class adminSkill(admin.ModelAdmin):
    list_display = ['name' , 'skill_type']

class adminJobPosition(admin.ModelAdmin):
    list_display = ['name']

class adminLocation(admin.ModelAdmin):
    list_display = ['city']

class adminHobby(admin.ModelAdmin):
    list_display = ['name']

class adminInterest(admin.ModelAdmin):
    list_display = ['name']

class adminEducation(admin.ModelAdmin):
    list_display = [ 'student','education_type' , 'institution_name' ,'board_or_university' , 'course_name' , 'passing_year']

class adminProject(admin.ModelAdmin):
    list_display = ['student' , 'project_title' , 'role' , 'start_date' , 'end_date']

admin.site.register(StudentProfile, adminStudent)
admin.site.register(Skill, adminSkill)
admin.site.register(JobPosition, adminJobPosition)
admin.site.register(JobLocation, adminLocation)
admin.site.register(Hobby, adminHobby)
admin.site.register(Interest , adminInterest)
admin.site.register(Education , adminEducation)
admin.site.register(Project , adminProject)
