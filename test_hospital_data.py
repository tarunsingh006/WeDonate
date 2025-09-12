import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organ_donation.settings')
django.setup()

from donors.models import DonationRequests, Appointments
from hospitals.models import User

# Test the exact query used in fetch_counts for hospital ID 1
hospital_id = 1
print(f"Testing for Hospital ID: {hospital_id}")

# Test appointment count
appointment_count = Appointments.objects.filter(hospital__id=hospital_id, appointment_status__iexact="Pending").count()
print(f"Appointment count: {appointment_count}")

# Test donation count  
donation_count = Appointments.objects.filter(
    hospital__id=hospital_id, 
    appointment_status__iexact="Approved", 
    donation_request__donation_status__iexact="Pending"
).count()
print(f"Donation count: {donation_count}")

# Show actual appointments
appointments = Appointments.objects.filter(hospital__id=hospital_id)
print(f"\nAll appointments for hospital {hospital_id}:")
for apt in appointments:
    print(f"  ID: {apt.id}, Status: {apt.appointment_status}, Donation Status: {apt.donation_request.donation_status}")