from django.db import models

from companies.models import CompanyProfile
from students.models import StudentProfile , Skill

# Create your models here.


class Qualification(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class JobRequirement(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='jobs')
    job_title = models.CharField(max_length=150)
    job_code = models.CharField(max_length=50, unique=True)
    job_description = models.TextField(blank=True)
    vacancies = models.PositiveIntegerField(default=1)
    salary_package = models.DecimalField(max_digits=12, decimal_places=2, help_text="Annual CTC in your currency")
    location = models.CharField(max_length=150, blank=True)
    experience = models.DecimalField(max_digits=4, decimal_places=1, default=0, help_text="Required experience in years")
    employment_type = models.CharField(max_length=50, choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Internship', 'Internship')], default='Full-time')
    required_skills = models.ManyToManyField(Skill, blank=True)
    required_qualifications = models.ManyToManyField(Qualification, blank=True)
    roles_and_responsibilities = models.TextField(blank=True)
    key_responsibilities = models.TextField(blank=True)
    posted_at = models.DateField(auto_now_add=True)
    application_deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company.company_name}"

class JobApplication(models.Model):

    class Stage(models.TextChoices):
        APPLIED = 'APPLIED', 'Applied'
        SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
        INTERVIEW = 'INTERVIEW', 'Interview Scheduled'
        SELECTED = 'SELECTED', 'Selected'
        REJECTED = 'REJECTED', 'Rejected'
        OPTED_OUT = 'OPTED_OUT', 'Opted Out'

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(JobRequirement, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    stage = models.CharField(
        max_length=20,
        choices=Stage.choices,
        default=Stage.APPLIED
    )

    def __str__(self):
        return f"{self.student.first_name} applied for {self.job.job_title}"