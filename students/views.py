from django.contrib import messages
import os
from django.shortcuts import render  , redirect , get_object_or_404
from .models import Hobby, Interest, JobLocation, JobPosition, Skill, StudentProfile , CompanyProfile  , Education , Project
from django.contrib.auth.decorators import login_required
from jobs.models import JobRequirement , JobApplication 
from django.core.paginator import Paginator

# Create your views here.
    
def home(request):

    featured_jobs = JobRequirement.objects.select_related(
        "company"
    ).prefetch_related(
        "required_skills"
    ).order_by("-posted_at")[:6]

    top_companies = CompanyProfile.objects.filter(
        is_active=True
    )[:8]

    context = {

        "featured_jobs": featured_jobs,

        "top_companies": top_companies,

        "total_students": StudentProfile.objects.count(),

        "total_companies": CompanyProfile.objects.count(),

        "total_jobs": JobRequirement.objects.count(),

        "total_applications": JobApplication.objects.count(),

    }

    return render(request, "home.html", context)


@login_required
def profile_view(request):
    if request.method == 'GET':
        # profile = request.user.student_profile
        profile, created = StudentProfile.objects.get_or_create(
    user=request.user,
    defaults={
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
    }
)
        applied_jobs = JobApplication.objects.filter(student=request.user.student_profile).count()
        shortlisted = JobApplication.objects.filter(student=request.user.student_profile, stage='SHORTLISTED').count()
        selected = JobApplication.objects.filter(student=request.user.student_profile, stage='selected').count()
        return render(request , 'profile.html' , {'profile': profile , 'applied_jobs': applied_jobs, 'shortlisted': shortlisted,
                                'selected': selected })
    else:
        pass

@login_required
def edit_student_profile(request):

        profile, created = StudentProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
            })

        if request.method == 'POST':

            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.save()

            
            profile.first_name = request.POST.get('first_name')
            profile.last_name = request.POST.get('last_name')
            profile.phone_number = request.POST.get('phone_number')
            profile.gender = request.POST.get('gender')
            # profile.date_of_birth = request.POST.get('date_of_birth')
            dob = request.POST.get('date_of_birth')
            if dob:
                profile.date_of_birth = dob
            else:
                profile.date_of_birth = None

            profile.location = request.POST.get('location')
            profile.experience = request.POST.get('experience')
            profile.github_url = request.POST.get('github_url') 
            profile.linkedin_url = request.POST.get('linkedin_url')

            if request.FILES.get('resume'):
                resume = request.FILES.get('resume')

                if resume:
                    allowed_extensions = [".pdf" , ".doc" , ".docx"]

                    extension = os.path.splitext(resume.name)[1].lower()

                    if extension not in allowed_extensions:
                        messages.error(
                            request , 
                            "Only PDF , DOC and DOCX files are allowed."
                        )
                        return redirect("edit_profile")

                    if resume.size > 5 * 1024 * 1024:
                        messages.error(
                            request,
                            "Resume size must be less than 5 MB."
                        )
                        return redirect("edit_profile")

                    profile.resume = resume
                    
            if request.FILES.get('profile_photo'):
                profile.profile_photo = request.FILES.get('profile_photo')

            profile.save()

            selected_skills = list(
                Skill.objects.filter(
                    id__in=request.POST.getlist('skills')
                )
            )

            new_skill = request.POST.get('new_skill' , "").strip()

            if new_skill:
                skill , created = Skill.objects.get_or_create(
                    name=new_skill.strip().title(),
                    defaults=
                    {
                        "skill_type": "TECHNICAL"
                    }
                )

                selected_skills.append(skill)   


            profile.skills.set(selected_skills)

            selected_hobbies = list(
                Hobby.objects.filter(
                    id__in=request.POST.getlist('hobbies')
                )
            )



            new_hobbies = request.POST.get('new_hobby')

            if new_hobbies:
                hobby , created = Hobby.objects.get_or_create(
                    name=new_hobbies.strip().title()
                )

                selected_hobbies.append(hobby)

            profile.hobbies.set(selected_hobbies)

            selected_interests = list(
                Interest.objects.filter(
                    id__in=request.POST.getlist('interests')
                )
            )

            new_interests = request.POST.get('new_interest')

            if new_interests:
                interest , created = Interest.objects.get_or_create(
                    name=new_interests.strip().title()
                )
                selected_interests.append(interest)

            profile.interests.set(selected_interests)

            print(request.POST.getlist("job_locations"))

            selected_job_locations = list(
                JobLocation.objects.filter(
                    id__in=request.POST.getlist('job_locations')
                )
            )

            new_job_locations = request.POST.get('new_location')

            if new_job_locations:
                job_location , created = JobLocation.objects.get_or_create(
                    city=new_job_locations.strip().title()
                )
                selected_job_locations.append(job_location)
            profile.job_locations.set(selected_job_locations)

            selected_job_positions = list(
                JobPosition.objects.filter(
                    id__in=request.POST.getlist('job_positions')
                )
            )

            new_job_positions = request.POST.get('new_position')

            if new_job_positions:
                job_position , created = JobPosition.objects.get_or_create(
                    name=new_job_positions.strip().title()
                )
                selected_job_positions.append(job_position)
            profile.job_positions.set(selected_job_positions)


            profile.skills.add(
                *Skill.objects.filter(
                    id__in=request.POST.getlist('skills')
                )
            )

            profile.hobbies.add(
                *Hobby.objects.filter(
                    id__in=request.POST.getlist('hobbies')
                )
            )

            profile.interests.add(
                *Interest.objects.filter(
                    id__in=request.POST.getlist('interests')
                )
            )

            profile.job_locations.add(
                *JobLocation.objects.filter(
                    id__in=request.POST.getlist('job_locations')
                )
            )

            profile.job_positions.add(
                *JobPosition.objects.filter(
                    id__in=request.POST.getlist('job_positions')
                )
            )


                

            messages.success(request, 'Profile updated successfully.')

            return redirect('profile')

        context = {
            'profile': profile,
            'skills': Skill.objects.all(),
            'hobbies': Hobby.objects.all(),
            'interests': Interest.objects.all(),
            'job_locations': JobLocation.objects.all(),
            'job_positions': JobPosition.objects.all(),
            'projects': profile.projects.all().order_by("-id"),
        }

        return render(request, 'edit_profile.html', context)

@login_required
def add_education(request):

    if request.method == "POST":

        profile = request.user.student_profile

        education_type = request.POST.get("education_type")
        institution_name = request.POST.get("institution_name")
        board_or_university = request.POST.get("board_or_university")
        course_name = request.POST.get("course_name")
        specialization = request.POST.get("specialization")
        percentage = request.POST.get("percentage") or None
        cgpa = request.POST.get("cgpa") or None
        passing_year = request.POST.get("passing_year")

        # Check duplicate education
        already_exists = Education.objects.filter(
            student=profile,
            education_type=education_type,
            institution_name=institution_name,
            board_or_university=board_or_university,
            course_name=course_name,
            specialization=specialization,
            passing_year=passing_year
        ).exists()

        if already_exists:
            messages.warning(
                request,
                "This education record already exists."
            )
            return redirect("edit_profile")


        Education.objects.create(

            student=profile,

            education_type=request.POST.get("education_type"),

            institution_name=request.POST.get("institution_name"),

            board_or_university=request.POST.get("board_or_university"),

            course_name=request.POST.get("course_name"),

            specialization=request.POST.get("specialization"),

            percentage=request.POST.get("percentage") or None,

            cgpa=request.POST.get("cgpa") or None,

            passing_year=request.POST.get("passing_year")

        )

        messages.success(request, "Education Added Successfully.")

    return redirect("edit_profile")

@login_required
def edit_education(request, id):

    education = get_object_or_404(
        Education,
        id=id,
        student=request.user.student_profile
    )

    if request.method == "POST":

        education_type = request.POST.get("education_type")
        institution_name = request.POST.get("institution_name")
        board_or_university = request.POST.get("board_or_university")
        course_name = request.POST.get("course_name")
        specialization = request.POST.get("specialization")
        percentage = request.POST.get("percentage") or None
        cgpa = request.POST.get("cgpa") or None
        passing_year = request.POST.get("passing_year")

        duplicate = Education.objects.filter(
            student=request.user.student_profile,
            education_type=education_type,
            institution_name=institution_name,
            board_or_university=board_or_university,
            course_name=course_name,
            specialization=specialization,
            passing_year=passing_year
        ).exclude(id=education.id).exists()

        if duplicate:
            messages.warning(
                request,
                "This education record already exists."
            )
            return redirect("edit_profile")

        education.education_type = education_type
        education.institution_name = institution_name
        education.board_or_university = board_or_university
        education.course_name = course_name
        education.specialization = specialization
        education.percentage = percentage
        education.cgpa = cgpa
        education.passing_year = passing_year

        education.save()

        messages.success(
            request,
            "Education Updated Successfully."
        )

    return redirect("edit_profile")

@login_required
def delete_education(request, id):

    education = get_object_or_404(
        Education,
        id=id,
        student=request.user.student_profile
    )

    education.delete()

    messages.success(request, "Education Deleted Successfully.")

    return redirect("edit_profile")


@login_required
def add_project(request):

    profile = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    if request.method == "POST":

        Project.objects.create(

            student=profile,

            project_title=request.POST.get("project_title"),

            project_description=request.POST.get("project_description"),

            technologies_used=request.POST.get("technologies_used"),

            role=request.POST.get("role"),

            github_url=request.POST.get("github_url"),

            live_url=request.POST.get("live_url"),

            start_date=request.POST.get("start_date"),

            end_date=request.POST.get("end_date") or None,

            currently_working=True if request.POST.get("currently_working") else False,

        )

        messages.success(
            request,
            "Project Added Successfully."
        )

        return redirect("edit_profile")

    return redirect("edit_profile")



@login_required
def edit_project(request, id):

    project = get_object_or_404(
        Project,
        id=id,
        student__user=request.user
    )

    if request.method == "POST":

        project.project_title = request.POST.get(
            "project_title"
        )

        project.project_description = request.POST.get(
            "project_description"
        )

        project.technologies_used = request.POST.get(
            "technologies_used"
        )

        project.role = request.POST.get(
            "role"
        )

        project.github_url = request.POST.get(
            "github_url"
        )

        project.live_url = request.POST.get(
            "live_url"
        )

        project.start_date = request.POST.get(
            "start_date"
        )

        end_date = request.POST.get(
            "end_date"
        )

        if end_date:
            project.end_date = end_date
        else:
            project.end_date = None

        project.currently_working = True if request.POST.get(
            "currently_working"
        ) else False

        project.save()

        messages.success(
            request,
            "Project Updated Successfully."
        )

        return redirect("edit_profile")


@login_required
def delete_project(request, id):

    project = get_object_or_404(

        Project,

        id=id,

        student__user=request.user

    )

    project.delete()

    messages.success(

        request,

        "Project Deleted Successfully."

    )

    return redirect("edit_profile")


@login_required
def student_dashboard(request):

    if request.method == 'GET':

        profile = request.user.student_profile

        applications = profile.applications.select_related(
            'job',
            'job__company'
        ).order_by('-applied_at')


        # ==============================
        # APPLICATION PAGINATION
        # ==============================

        paginator = Paginator(
            applications,
            5
        )

        page_number = request.GET.get('page')

        applications_page = paginator.get_page(
            page_number
        )


        # ==============================
        # LATEST JOBS
        # ==============================

        latest_jobs = JobRequirement.objects.order_by(
            '-posted_at'
        )[:5]


        # ==============================
        # STATISTICS
        # ==============================

        total_jobs = JobRequirement.objects.count()

        applied_jobs = JobApplication.objects.filter(
            student=request.user.student_profile
        ).count()

        shortlisted = JobApplication.objects.filter(
            student=request.user.student_profile,
            stage='SHORTLISTED'
        ).count()

        selected = JobApplication.objects.filter(
            student=request.user.student_profile,
            stage='selected'
        ).count()


        # ==============================
        # APPLIED JOB IDs
        # ==============================

        appliedJobs = []

        try:

            student = request.user.student_profile

            appliedJobs = JobApplication.objects.filter(
                student=student
            ).values_list(
                "job_id",
                flat=True
            )

        except StudentProfile.DoesNotExist:

            pass


        return render(
            request,
            'dashboard.html',
            {
                'total_jobs': total_jobs,

                'applied_jobs': applied_jobs,

                'shortlisted': shortlisted,

                'selected': selected,

                # Keep the same context name
                'applications': applications_page,

                # Additional pagination object
                'applications_page': applications_page,

                'latest_jobs': latest_jobs,

                'appliedJobs': appliedJobs,
            }
        )