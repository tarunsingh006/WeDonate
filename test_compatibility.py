#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organ_donation.settings')
django.setup()

from ml_matching.matching_algorithm import OrganMatchingML

# Test the compatibility
ml_matcher = OrganMatchingML()

# Test O- donor to O- recipient
donor_data = {
    'blood_type': 'O-',
    'organ_type': 'Kidney',
    'age': 30,
    'weight': 70,
    'smoking_status': False,
    'alcohol_consumption': False
}

hospital_req = {
    'blood_type': 'O-',
    'organ_type': 'Kidney',
    'patient_age': 40,
    'patient_weight': 70,
    'urgency_level': 'Medium'
}

print("Testing O- donor to O- recipient:")
print(f"Blood compatibility: {ml_matcher.blood_compatibility('O-', 'O-')}")
score = ml_matcher.calculate_compatibility_score(donor_data, hospital_req)
print(f"Compatibility score: {score}")

print("\nTesting O- donor to A+ recipient:")
hospital_req['blood_type'] = 'A+'
print(f"Blood compatibility: {ml_matcher.blood_compatibility('O-', 'A+')}")
score = ml_matcher.calculate_compatibility_score(donor_data, hospital_req)
print(f"Compatibility score: {score}")

print("\nTesting A+ donor to O- recipient:")
donor_data['blood_type'] = 'A+'
hospital_req['blood_type'] = 'O-'
print(f"Blood compatibility: {ml_matcher.blood_compatibility('A+', 'O-')}")
score = ml_matcher.calculate_compatibility_score(donor_data, hospital_req)
print(f"Compatibility score: {score}")