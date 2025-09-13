#!/usr/bin/env python3
"""
Standalone runner for the Organ Matching ML Algorithm
"""

import sys
import os
sys.path.append('ml_matching')

# Mock Django imports
import types
django_module = types.ModuleType('django')
django_module.db = types.ModuleType('db')
django_module.db.models = types.ModuleType('models')
django_module.db.models.Q = type('Q', (), {})
sys.modules['django'] = django_module
sys.modules['django.db'] = django_module.db
sys.modules['django.db.models'] = django_module.db.models

donors_module = types.ModuleType('donors')
donors_module.models = types.ModuleType('models')
donors_module.models.DonationRequests = type('DonationRequests', (), {'objects': None})
sys.modules['donors'] = donors_module
sys.modules['donors.models'] = donors_module.models

from matching_algorithm import OrganMatchingML

def main():
    print("Organ Matching ML Algorithm - Standalone Runner")
    print("=" * 50)
    
    # Initialize the algorithm
    matcher = OrganMatchingML()
    
    # Train the model
    print("Training the ML model...")
    try:
        accuracy = matcher.train_model()
        print(f"Model trained successfully with accuracy: {accuracy:.4f}")
    except Exception as e:
        print(f"Error during training: {e}")
        return
    
    # Test prediction
    print("\nTesting prediction...")
    
    donor_data = {
        'blood_type': 'O-',
        'organ_type': 'Kidney',
        'age': 25,
        'weight': 70,
        'smoking_status': False,
        'alcohol_consumption': False
    }
    
    hospital_req = {
        'blood_type': 'A+',
        'organ_type': 'Kidney',
        'urgency_level': 'Critical',
        'patient_age': 30,
        'patient_weight': 65
    }
    
    try:
        prediction, probability = matcher.predict_match(donor_data, hospital_req)
        compatibility_score = matcher.calculate_compatibility_score(donor_data, hospital_req)
        
        print(f"Donor: {donor_data['blood_type']} {donor_data['organ_type']}, Age: {donor_data['age']}")
        print(f"Recipient: {hospital_req['blood_type']} {hospital_req['organ_type']}, Age: {hospital_req['patient_age']}")
        print(f"Compatibility Score: {compatibility_score}%")
        print(f"ML Prediction: {'Match' if prediction == 1 else 'No Match'}")
        print(f"Match Probability: {probability:.4f}")
        
    except Exception as e:
        print(f"Error during prediction: {e}")
    
    print("\nAlgorithm execution completed!")

if __name__ == "__main__":
    main()