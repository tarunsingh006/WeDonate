#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organ_donation.settings')
django.setup()

from donors.models import DonationRequests, Appointments
from hospitals.models import User

print("=== DONATION REQUESTS ===")
for req in DonationRequests.objects.all():
    print(f"ID: {req.id}, Donor: {req.donor.first_name}, Organ: {req.organ_type}, Status: {req.donation_status}")

print("\n=== APPOINTMENTS ===")
for apt in Appointments.objects.all():
    print(f"ID: {apt.id}, Hospital: {apt.hospital.hospital_name}, Donor: {apt.donation_request.donor.first_name}, Status: {apt.appointment_status}")

print("\n=== HOSPITALS ===")
for hosp in User.objects.filter(is_staff=True):
    print(f"ID: {hosp.id}, Name: {hosp.hospital_name}")

print(f"\nTotal Donation Requests: {DonationRequests.objects.count()}")
print(f"Total Appointments: {Appointments.objects.count()}")
print(f"Total Hospitals: {User.objects.filter(is_staff=True).count()}")