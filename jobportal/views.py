from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Application, Profile, Job
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm, JobForm
from .models import Job, Application
from django.db.models import Q
from django.contrib import messages


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            role = user.profile.role
            if role == 'employer':
                return redirect('employer_dashboard')  # Create this view
            elif role == 'applicant':
                return redirect('applicant_dashboard')  # Create this view
        else:
            return render(request, 'auth/login.html', {'error': 'Invalid username or password'})
    return render(request, 'auth/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        role = request.POST['role']

        if password1 != password2:
            return render(request, 'auth/register.html', {'error': "Passwords do not match"})

        user = User.objects.create_user(username=username, email=email, password=password1)
        Profile.objects.create(user=user, role=role)
        login(request, user)
        return redirect('login') 
    return render(request, "auth/register.html")


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def employer_dashboard(request):
    if request.user.profile.role != 'employer':
        return redirect('login')  # Optional: or show 403 error
    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'employer/dashboard.html', {'jobs': jobs})


@login_required
def post_job(request):
    if request.user.profile.role != 'employer':
        return redirect('login')  # or raise 403

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('employer_dashboard')
    else:
        form = JobForm()
    return render(request, 'employer/post_job.html', {'form': form})



@login_required
def job_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    applications = Application.objects.filter(job=job)

    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        action = request.POST.get('action')
        application = get_object_or_404(Application, id=app_id, job=job)

        if action in ['Approved', 'Rejected']:
            application.status = action
            application.save()

        return redirect('job_applications', job_id=job_id)

    return render(request, 'employer/job_applications.html', {
        'job': job,
        'applications': applications
    })


@login_required
def applicant_dashboard(request):
    if request.user.profile.role != 'applicant':
        return redirect('login')  # Or raise PermissionDenied
    applications = Application.objects.filter(applicant=request.user).select_related('job')
    return render(request, 'applicant/dashboard.html', {'applications': applications})




@login_required
def applicant_job_list(request):
    if request.user.profile.role != 'applicant':
        return redirect('login')

    query = request.GET.get('q')
    jobs = Job.objects.all().order_by('-created_at')

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(location__icontains=query)
        )

    # Get job IDs the current user has applied to
    applied_job_ids = Application.objects.filter(applicant=request.user).values_list('job_id', flat=True)

    return render(request, 'applicant/job_list.html', {
        'jobs': jobs,
        'query': query,
        'applied_job_ids': applied_job_ids,
    })




@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    
    # Prevent duplicate application
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('applicant_job_list')

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('applicant_dashboard')
    else:
        form = ApplicationForm()

    return render(request, 'applicant/apply_job.html', {
        'form': form,
        'job': job
    })

@login_required
def my_applications(request):
    status_filter = request.GET.get('status')
    applications = Application.objects.filter(applicant=request.user)

    if status_filter in ['Pending', 'Approved', 'Rejected']:
        applications = applications.filter(status=status_filter)

    return render(request, 'applicant/my_applications.html', {
        'applications': applications,
        'status_filter': status_filter,
    })


# @login_required
# def applied_jobs(request):
#     if request.user.profile.role != 'applicant':
#         return redirect('login')

#     applications = Application.objects.select_related('job').filter(applicant=request.user).order_by('-applied_at')

#     return render(request, 'applicant/applied_jobs.html', {
#         'applications': applications
#     })