from django.shortcuts import render , redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import JobApplication , JobRequirement 
from students.models import StudentProfile
from django.db.models import Q

# Create your views here.



def job_list(request):

    jobs = JobRequirement.objects.select_related(
        "company"
    ).prefetch_related(
        "required_skills",
        "required_qualifications"
    )

    keyword = request.GET.get("keyword")
    location = request.GET.get("location")
    experience = request.GET.get("experience")
    employment_type = request.GET.get("employment_type")

    if keyword:
        jobs = jobs.filter(
            Q(job_title__icontains=keyword) |
            Q(company__company_name__icontains=keyword) |
            Q(job_description__icontains=keyword) |
            Q(company__company_name__icontains=keyword) |
            Q(required_skills__name__icontains=keyword)
        ).distinct()

    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    if experience:
        jobs = jobs.filter(
            experience__lte=experience
        )

    if employment_type:
        jobs = jobs.filter(
            employment_type=employment_type
        )

    jobs = jobs.order_by("-posted_at")

    applied_jobs = []

    if request.user.is_authenticated:

        try:

            student = request.user.student_profile

            applied_jobs = JobApplication.objects.filter(
                student=student
            ).values_list(
                "job_id",
                flat=True
            )

        except StudentProfile.DoesNotExist:
            pass

    context = {

        "jobs": jobs,

        "keyword": keyword,

        "location": location,

        "experience": experience,

        "employment_type": employment_type,

        "applied_jobs": applied_jobs,

    }

    return render(
        request,
        "job_list.html",
        context
    )




@login_required
def job_detail(request, id):

    job = get_object_or_404(
        JobRequirement.objects.select_related("company")
        .prefetch_related(
            "required_skills",
            "required_qualifications"
        ),
        id=id
    )

    similar_jobs = JobRequirement.objects.filter(
        job_title__icontains=job.job_title.split()[0]
    ).exclude(
        id=job.id
    )[:5]


    already_applied = False
    student = None
    experience_mismatch = False

    if hasattr(request.user, "student_profile"):

        student = request.user.student_profile

        already_applied = job.applications.filter(
            student=request.user.student_profile
        ).exists()

    if not already_applied:
        experience_mismatch = student.experience < job.experience

    context = {

        "job": job,

        "student": student,

        "similar_jobs": similar_jobs,

        "already_applied": already_applied,

        "experience_mismatch": experience_mismatch

    }

    return render(
        request,
        "job_details.html",
        context
    )


@login_required
def apply_job(request, id):

    

    student = request.user.student_profile

    

    job = get_object_or_404(
        JobRequirement,
        id=id
    )

    if not student.resume:
                messages.error(
                    request,
                    "Please upload your resume before applying for a job."
                )
                return redirect("job_detail",id=job.id)

    # Experience check 
    if student.experience < job.experience and not request.GET.get("force"):

        messages.warning(
            request, 
            f"This job recommends {job.experience} years of experience. You have {student.experience} years."
        )

        return redirect("job_detail" , id = job.id)

    already_applied = JobApplication.objects.filter(
        student=student,
        job=job
    ).exists()

    if already_applied:

        messages.warning(
            request,
            "You have already applied for this job."
        )

        return redirect(
            "job_detail",
            id=job.id
        )

    JobApplication.objects.create(

        student=student,

        job=job,

        stage=JobApplication.Stage.APPLIED

    )

    messages.success(
        request,
        "Job Applied Successfully."
    )

    return redirect(
        "job_detail",
        id=job.id
    )


@login_required
def applied_jobs(request):

    applications = JobApplication.objects.filter(
        student=request.user.student_profile
    ).select_related(
        "job",
        "job__company"
    ).order_by("-applied_at")

    return render(
        request,
        "applied_jobs.html",
        {
            "applications": applications
        }
    )
