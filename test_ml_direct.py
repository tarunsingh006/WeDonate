import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeDonate.settings')
django.setup()

from donors.models import DonationRequests
from ml_matching.matching_algorithm import OrganMatchingML

# Test ML matching directly
donations = DonationRequests.objects.filter(donation_status='Pending')
print(f"Found {donations.count()} pending donations")

ml_matcher = OrganMatchingML()

# Test with Kidney + O- requirement
test_req = {
    'blood_type': 'O-',
    'organ_type': 'Kidney',
    'patient_age': 35,
    'patient_weight': 70,
    'urgency_level': 'Medium'
}

print(f"Testing requirement: {test_req}")

for donation in donations:
    donor_data = {
        'blood_type': donation.blood_type,
        'organ_type': donation.organ_type,
        'age': 30,
        'weight': 70,
        'smoking_status': False,
        'alcohol_consumption': False
    }
    
    score = ml_matcher.calculate_compatibility_score(donor_data, test_req)
    print(f"Donor {donation.donor.first_name}: {donation.organ_type} {donation.blood_type} -> {score}%")