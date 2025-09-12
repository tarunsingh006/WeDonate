import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organ_donation.settings')
django.setup()

from donors.models import DonationRequests, Appointments
from hospitals.models import User

print("=== DEBUG DATA ===")

# Check hospitals
hospitals = User.objects.filter(is_staff=True)
print(f"Hospitals count: {hospitals.count()}")
for hospital in hospitals:
    print(f"Hospital ID: {hospital.id}, Name: {hospital.hospital_name}, Username: {hospital.username}")

# Check donation requests
donations = DonationRequests.objects.all()
print(f"\nDonation requests count: {donations.count()}")
for donation in donations:
    print(f"Donation ID: {donation.id}, Organ: {donation.organ_type}, Status: {donation.donation_status}")

# Check appointments
appointments = Appointments.objects.all()
print(f"\nAppointments count: {appointments.count()}")
for appointment in appointments:
    print(f"Appointment ID: {appointment.id}, Hospital ID: {appointment.hospital.id if appointment.hospital else 'None'}, Status: {appointment.appointment_status}")

print("\n=== END DEBUG ===")