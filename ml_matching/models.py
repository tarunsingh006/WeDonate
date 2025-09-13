from django.db import models
from hospitals.models import User

class HospitalOrganRequirement(models.Model):
    ORGAN_CHOICES = [
        ('Heart', 'Heart'),
        ('Kidney', 'Kidney'),
        ('Liver', 'Liver'),
        ('Lungs', 'Lungs'),
        ('Pancreas', 'Pancreas'),
        ('Cornea', 'Cornea'),
    ]
    
    BLOOD_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    URGENCY_CHOICES = [
        ('Critical', 'Critical'),
        ('Urgent', 'Urgent'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    
    hospital = models.ForeignKey(User, on_delete=models.CASCADE)
    organ_type = models.CharField(max_length=20, choices=ORGAN_CHOICES)
    blood_type = models.CharField(max_length=3, choices=BLOOD_CHOICES)
    patient_age = models.IntegerField()
    patient_weight = models.FloatField()
    urgency_level = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    additional_notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.hospital.hospital_name} - {self.organ_type} ({self.urgency_level})"

class DonorMedicalProfile(models.Model):
    donor = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    smoking_status = models.BooleanField(default=False)
    alcohol_consumption = models.BooleanField(default=False)
    medical_conditions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.donor.first_name} - Medical Profile"