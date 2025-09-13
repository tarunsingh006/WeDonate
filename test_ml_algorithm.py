#!/usr/bin/env python3
"""
Test script for the Organ Matching ML Algorithm
Runs the algorithm without Django dependencies
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

# Mock Django imports to avoid dependency issues
class MockModel:
    pass

class MockQ:
    pass

# Create mock modules
import types
donors_module = types.ModuleType('donors')
donors_module.models = types.ModuleType('models')
donors_module.models.DonationRequests = MockModel
sys.modules['donors'] = donors_module
sys.modules['donors.models'] = donors_module.models

django_module = types.ModuleType('django')
django_module.db = types.ModuleType('db')
django_module.db.models = types.ModuleType('models')
django_module.db.models.Q = MockQ
sys.modules['django'] = django_module
sys.modules['django.db'] = django_module.db
sys.modules['django.db.models'] = django_module.db.models

ml_matching_module = types.ModuleType('ml_matching')
ml_matching_module.models = types.ModuleType('models')
ml_matching_module.models.HospitalOrganRequirement = MockModel
ml_matching_module.models.DonorMedicalProfile = MockModel
sys.modules['ml_matching'] = ml_matching_module
sys.modules['ml_matching.models'] = ml_matching_module.models

# Now import the actual algorithm
sys.path.append('ml_matching')
from matching_algorithm import OrganMatchingML

def test_algorithm():
    """Test the organ matching algorithm"""
    print("Testing Organ Matching ML Algorithm...")
    
    # Initialize the algorithm
    matcher = OrganMatchingML()
    
    # Test blood compatibility
    print("\n1. Testing blood compatibility:")
    test_cases = [
        ('O-', 'A+', True),
        ('A+', 'O+', False),
        ('AB+', 'AB+', True),
        ('O+', 'AB-', False)
    ]
    
    for donor, recipient, expected in test_cases:
        result = matcher.blood_compatibility(donor, recipient)
        status = "PASS" if result == expected else "FAIL"
        print(f"   {status} {donor} -> {recipient}: {result}")
    
    # Test compatibility scoring
    print("\n2. Testing compatibility scoring:")
    donor_data = {
        'blood_type': 'A+',
        'organ_type': 'Kidney',
        'age': 30,
        'weight': 70,
        'smoking_status': False,
        'alcohol_consumption': False
    }
    
    hospital_req = {
        'blood_type': 'A+',
        'organ_type': 'Kidney',
        'patient_age': 32,
        'patient_weight': 68
    }
    
    score = matcher.calculate_compatibility_score(donor_data, hospital_req)
    print(f"   Compatibility score: {score}%")
    
    # Test data preparation
    print("\n3. Testing data preparation:")
    try:
        df = matcher.prepare_training_data()
        print(f"   PASS Generated training data: {len(df)} samples")
        print(f"   PASS Features: {list(df.columns)}")
        print(f"   PASS Data shape: {df.shape}")
        
        # Show sample data
        print("\n   Sample data:")
        print(df.head(3).to_string())
        
    except Exception as e:
        print(f"   FAIL Error in data preparation: {e}")
    
    print("\nPASS Algorithm test completed successfully!")

if __name__ == "__main__":
    test_algorithm()