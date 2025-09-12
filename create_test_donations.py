import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organ_donation.settings')
django.setup()

from donors.models import DonationRequests, Appointments
from hospitals.models import User
from django.contrib.auth import get_user_model

# Get hospital users
hospital1 = User.objects.get(id=1)  # rajesh
hospital4 = User.objects.get(id=4)  # maxhospital

# Get donor users (non-staff users)
donors = User.objects.filter(is_staff=False)
print(f"Found {donors.count()} donors")

if donors.count() > 0:
    donor = donors.first()
    print(f"Using donor: {donor.username}")
    
    # Create a new donation request
    donation = DonationRequests.objects.create(
        donor=donor,
        organ_type="Heart",
        blood_type="O+",
        donation_status="Pending",
        family_relation_name="John Doe",
        family_relation="Brother",
        family_contact_number="1234567890"
    )
    print(f"Created donation request ID: {donation.id}")
    
    # Create an approved appointment for this donation
    appointment = Appointments.objects.create(
        donation_request=donation,
        hospital=hospital1,
        date="2024-01-15",
        time="10:00:00",
        appointment_status="Approved"
    )
    print(f"Created approved appointment ID: {appointment.id}")
    
    print("Now hospital should see 1 pending donation!")
else:
    print("No donors found. Please create a donor user first.")