from django.db import models
from django.conf import settings
from companies.models import CompanyProfile
# Create your models here.

class StudentProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10 , blank=True)
    date_of_birth = models.DateField(
        blank=True,
        null=True
    )
    
    phone_number = models.CharField(max_length=15 , blank=True)

    location = models.CharField(max_length=100 , blank=True)

    profile_photo = models.ImageField(
    upload_to="student_profiles/",
    blank=True,
    null=True
    )

    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    experience = models.DecimalField(
        max_digits=4, 
        decimal_places=1, 
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Many-to-Many relationshp 

    skills = models.ManyToManyField(
        "Skill",
        blank=True
    )

    hobbies = models.ManyToManyField(
        "Hobby",
        blank=True
    )

    interests = models.ManyToManyField(
        "Interest",
        blank=True
    )

    job_positions = models.ManyToManyField(
        "JobPosition",
        blank=True
    )

    job_locations = models.ManyToManyField(
        "JobLocation",
        blank=True
    )

    def __str__(self):
        return self.first_name


class Education(models.Model):

    EDUCATION_CHOICES = [
        ("10TH", "10th"),
        ("12TH", "12th"),
        ("GRADUATION", "Graduation"),
        ("POST_GRADUATION", "Post Graduation"),
        ("OTHER", "Other"),
    ]

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="educational_background"
    )

    education_type = models.CharField(
        max_length=30,
        choices=EDUCATION_CHOICES
    )

    institution_name = models.CharField(
        max_length=200
    )

    board_or_university = models.CharField(
        max_length=200
    )

    course_name = models.CharField(
        max_length=200,
        blank=True
    )

    specialization = models.CharField(
        max_length=200,
        blank=True
    )

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True
    )

    passing_year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.student.first_name} - {self.education_type}"

    
class Skill(models.Model):

    SKILL_TYPE = [
        ("TECHNICAL", "Technical"),
        ("SOFT", "Soft"),
    ]

    name = models.CharField(
        max_length=100,
        unique=True
    )

    skill_type = models.CharField(
        max_length=20,
        choices=SKILL_TYPE
    )

    def __str__(self):
        return self.name


class Hobby(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name

class Interest(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class JobPosition(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class JobLocation(models.Model):

    city = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.city


class Project(models.Model):

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    project_title = models.CharField(
        max_length=200
    )

    project_description = models.TextField()

    technologies_used = models.CharField(
        max_length=300
    )

    role = models.CharField(
        max_length=150,
        blank=True
    )

    github_url = models.URLField(
        blank=True
    )

    live_url = models.URLField(
        blank=True
    )

    start_date = models.DateField()

    end_date = models.DateField(
        blank=True,
        null=True
    )

    currently_working = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.project_title