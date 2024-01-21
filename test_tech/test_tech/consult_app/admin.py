from django.contrib import admin
from .models import AppUser, Patient, Doctor

admin.site.register(AppUser)
admin.site.register(Patient)
admin.site.register(Doctor)