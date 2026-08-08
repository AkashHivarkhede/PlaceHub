from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('profile/' , views.profile_view , name='profile'),
  path('edit_profile/' , views.edit_student_profile , name='edit_profile'),
  path('education/add/' , views.add_education , name='add_education'),
  path("education/edit/<int:id>/", views.edit_education, name="edit_education"),
  path("education/delete/<int:id>/", views.delete_education, name="delete_education"),
  path("project/add/", views.add_project, name="add_project"),
  path("project/edit/<int:id>/", views.edit_project, name="edit_project"),
  path("project/delete/<int:id>/", views.delete_project, name="delete_project"),
  path('student_dashboard/' , views.student_dashboard , name='student_dashboard'),
]