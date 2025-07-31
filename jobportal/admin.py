from django.contrib import admin
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'posted_by', 'created_at')
    search_fields = ('title', 'company_name', 'location')
    list_filter = ('location', 'company_name')
    ordering = ('-created_at',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job__title', 'applicant', 'applied_at')
    search_fields = ('job__title', 'applicant__username', 'applicant__email')
    list_filter = ('applied_at',)
    ordering = ('-applied_at',)