import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organ_donation.settings')
django.setup()

from donors.models import DonationRequests, Appointments
from hospitals.models import User

# Check existing users
all_users = User.objects.all()
print("All users:")
for user in all_users:
    print(f"ID: {user.id}, Username: {user.username}, Staff: {user.is_staff}")

# Get hospital user
hospital = User.objects.filter(is_staff=True).first()
if not hospital:
    print("No hospital users found!")
    exit()

print(f"Using hospital: {hospital.username} (ID: {hospital.id})")

# Get or create a donor user
donor = User.objects.filter(is_staff=False).first()
if not donor:
    # Create a donor user
    donor = User.objects.create_user(
        username="testdonor",
        password="testpass123",
        email="donor@test.com",
        first_name="Test",
        last_name="Donor",
        is_staff=False
    )
    print(f"Created donor: {donor.username}")
else:
    print(f"Using existing donor: {donor.username}")

# Create a new donation request
donation = DonationRequests.objects.create(
    donor=donor,
    organ_type="Heart",
    blood_type="O+",
    donation_status="Pending",
    family_relation_name="John Doe",
    family_relation="Brother",
    family_contact_number="1234567890",
    donated_before=False,
    family_consent=True
)
print(f"Created donation request ID: {donation.id}")

# Create an approved appointment for this donation
appointment = Appointments.objects.create(
    donation_request=donation,
    hospital=hospital,
    date="2024-01-15",
    time="10:00:00",
    appointment_status="Approved"
)
print(f"Created approved appointment ID: {appointment.id}")

print("✅ Test data created! Hospital should now see 1 pending donation.")