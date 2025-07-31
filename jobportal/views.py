from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import render, redirect
from .models import Profile, Job
from django.contrib.auth.decorators import login_required

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


def applicant_dashboard(request):
    pass