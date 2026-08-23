# accounts/admin.py
from django.contrib import admin
from .models import UserProfile, StudyRecord

admin.site.register(UserProfile)
admin.site.register(StudyRecord)