from django.urls import path
from . import views
urlpatterns = [
    path('job_list/' , views.job_list , name='job_list'),
  path('job_detail/<int:id>/' , views.job_detail , name='job_detail'),
  path("job/apply/<int:id>/", views.apply_job, name="apply_job"),
  path('applied_jobs/' , views.applied_jobs , name='applied_jobs'), 
]