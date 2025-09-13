import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organ_donation.settings')
django.setup()

from ml_matching.matching_algorithm import OrganMatchingML

def main():
    print("Training ML Model for Organ Donation Matching...")
    
    ml_matcher = OrganMatchingML()
    accuracy = ml_matcher.train_model()
    
    print(f"✅ Model trained successfully with accuracy: {accuracy:.2f}")
    print("Model saved to: ml_matching/trained_model.joblib")
    
    # Test the model
    print("\n🧪 Testing the model...")
    
    # Sample donor data
    donor_data = {
        'blood_type': 'O+',
        'organ_type': 'Heart',
        'age': 35,
        'weight': 70.0,
        'smoking_status': False,
        'alcohol_consumption': False
    }
    
    # Sample hospital requirement
    hospital_req = {
        'blood_type': 'O+',
        'organ_type': 'Heart',
        'urgency_level': 'Critical',
        'patient_age': 40,
        'patient_weight': 75.0
    }
    
    prediction, probability = ml_matcher.predict_match(donor_data, hospital_req)
    compatibility_score = ml_matcher.calculate_compatibility_score(donor_data, hospital_req)
    
    print(f"Donor: {donor_data['organ_type']} - {donor_data['blood_type']}")
    print(f"Hospital Requirement: {hospital_req['organ_type']} - {hospital_req['blood_type']}")
    print(f"Match Prediction: {'✅ MATCH' if prediction == 1 else '❌ NO MATCH'}")
    print(f"ML Probability: {probability:.2f}")
    print(f"Compatibility Score: {compatibility_score}%")

if __name__ == "__main__":
    main()