#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organ_donation.settings')
django.setup()

from donors.models import DonationRequests

print("=== DONATION REQUESTS WITH BLOOD TYPES ===")
for req in DonationRequests.objects.all():
    print(f"ID: {req.id}, Donor: {req.donor.first_name}, Organ: {req.organ_type}, Blood: {req.blood_type}, Status: {req.donation_status}")

# Check if there are any Kidney + O- combinations
kidney_o_neg = DonationRequests.objects.filter(organ_type='Kidney', blood_type='O-')
print(f"\nKidney + O- donations: {kidney_o_neg.count()}")

# Check all blood types
blood_types = DonationRequests.objects.values_list('blood_type', flat=True).distinct()
print(f"All blood types in DB: {list(blood_types)}")

# Check all organ types  
organ_types = DonationRequests.objects.values_list('organ_type', flat=True).distinct()
print(f"All organ types in DB: {list(organ_types)}")