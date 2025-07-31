from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/post-job/', views.post_job, name='post_job'),
    path('employer/job/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),

    path('applicant/dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('applicant/jobs/', views.applicant_job_list, name='applicant_job_list'),
    path('applicant/job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('applicant/applied-jobs/', views.applied_jobs, name='applied_jobs'),

    
]