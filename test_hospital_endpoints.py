import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organ_donation.settings')
django.setup()

from donors.models import DonationRequests, Appointments
from hospitals.models import User

# Test data for hospital ID 2 (maxhospital)
hospital_id = 2
print(f"Testing endpoints for Hospital ID: {hospital_id}")

# Test fetch_appointments query
appointments = Appointments.objects.filter(hospital__id=hospital_id, appointment_status__iexact="Pending")
print(f"Pending appointments: {appointments.count()}")
for apt in appointments:
    print(f"  - Appointment {apt.id}: {apt.donation_request.donor.first_name} {apt.donation_request.donor.last_name}")

# Test fetch_donations query  
donations = Appointments.objects.filter(
    hospital__id=hospital_id,
    appointment_status__iexact="Approved", 
    donation_request__donation_status__iexact="Pending"
)
print(f"Pending donations: {donations.count()}")
for don in donations:
    print(f"  - Donation {don.donation_request.id}: {don.donation_request.organ_type} from {don.donation_request.donor.first_name}")

# Test fetch_counts query
appointment_count = Appointments.objects.filter(hospital__id=hospital_id, appointment_status__iexact="Pending").count()
donation_count = Appointments.objects.filter(
    hospital__id=hospital_id,
    appointment_status__iexact="Approved", 
    donation_request__donation_status__iexact="Pending"
).count()

print(f"\nCounts - Appointments: {appointment_count}, Donations: {donation_count}")