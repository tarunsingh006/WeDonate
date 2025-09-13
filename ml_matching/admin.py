from django.contrib import admin
from .models import HospitalOrganRequirement, DonorMedicalProfile

@admin.register(HospitalOrganRequirement)
class HospitalOrganRequirementAdmin(admin.ModelAdmin):
    list_display = ['hospital', 'organ_type', 'blood_type', 'urgency_level', 'patient_age', 'created_at', 'is_active']
    list_filter = ['organ_type', 'blood_type', 'urgency_level', 'is_active']
    search_fields = ['hospital__hospital_name', 'organ_type']

@admin.register(DonorMedicalProfile)
class DonorMedicalProfileAdmin(admin.ModelAdmin):
    list_display = ['donor', 'age', 'weight', 'height', 'smoking_status', 'alcohol_consumption']
    list_filter = ['smoking_status', 'alcohol_consumption']
    search_fields = ['donor__username', 'donor__first_name', 'donor__last_name']