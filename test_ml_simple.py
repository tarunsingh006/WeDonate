#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('c:\\all Learnings\\GitHub\\WeDonate')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeDonate.settings')
django.setup()

from donors.models import DonationRequests
from ml_matching.matching_algorithm import OrganMatchingML

def test_ml_matching():
    print("Testing ML Matching System...")
    
    # Get all pending donations
    donations = DonationRequests.objects.filter(donation_status='Pending')
    print(f"Found {donations.count()} pending donations:")
    
    for donation in donations:
        print(f"  - ID: {donation.id}, Donor: {donation.donor.first_name}, Organ: {donation.organ_type}, Blood: {donation.blood_type}")
    
    # Initialize ML matcher
    ml_matcher = OrganMatchingML()
    
    # Test with simple requirement
    test_req = {
        'blood_type': 'O-',
        'organ_type': 'Kidney', 
        'patient_age': 35,
        'patient_weight': 70,
        'urgency_level': 'Medium'
    }
    
    print(f"\nTesting with requirement: {test_req}")
    print("\nCompatibility Scores:")
    
    matches = []
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
        print(f"  - {donation.donor.first_name} ({donation.organ_type}, {donation.blood_type}): {score}%")
        
        if score > 0:
            matches.append({
                'donor': donation.donor.first_name,
                'organ': donation.organ_type,
                'blood': donation.blood_type,
                'score': score
            })
    
    print(f"\nFound {len(matches)} potential matches")
    matches.sort(key=lambda x: x['score'], reverse=True)
    
    print("\nTop matches:")
    for match in matches[:5]:
        print(f"  - {match['donor']} ({match['organ']}, {match['blood']}): {match['score']}%")

if __name__ == "__main__":
    test_ml_matching()