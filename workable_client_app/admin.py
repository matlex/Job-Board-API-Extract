from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import *


@register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'job', 'status', 'phone', 'email']


@register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'full_title', 'department', 'wk_short_code']
