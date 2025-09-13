import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organ_donation.settings')
django.setup()

from ml_matching.matching_algorithm import OrganMatchingML
from donors.models import DonationRequests
from ml_matching.models import HospitalOrganRequirement, DonorMedicalProfile
from hospitals.models import User

def create_test_data():
    """Create test data for ML matching"""
    print("🔧 Creating test data...")
    
    # Get or create hospital user
    hospital = User.objects.filter(is_staff=True).first()
    if not hospital:
        hospital = User.objects.create_user(
            username="test_hospital",
            password="testpass123",
            email="hospital@test.com",
            first_name="Test",
            last_name="Hospital",
            is_staff=True,
            hospital_name="City General Hospital"
        )
    
    # Get or create donor user
    donor = User.objects.filter(is_staff=False).first()
    if not donor:
        donor = User.objects.create_user(
            username="test_donor",
            password="testpass123",
            email="donor@test.com",
            first_name="John",
            last_name="Donor",
            is_staff=False
        )
    
    # Create donor medical profile
    donor_profile, created = DonorMedicalProfile.objects.get_or_create(
        donor=donor,
        defaults={
            'age': 35,
            'weight': 70.0,
            'height': 175.0,
            'blood_type': 'O+',
            'medical_history': 'Healthy individual with no major medical issues',
            'smoking_status': False,
            'alcohol_consumption': False,
            'chronic_diseases': 'None',
            'medications': 'None'
        }
    )
    
    # Create donation request
    donation, created = DonationRequests.objects.get_or_create(
        donor=donor,
        organ_type="Heart",
        defaults={
            'blood_type': 'O+',
            'donation_status': 'Pending',
            'family_relation_name': 'Jane Donor',
            'family_relation': 'Spouse',
            'family_contact_number': '1234567890',
            'donated_before': False,
            'family_consent': True
        }
    )
    
    # Create hospital organ requirement
    requirement, created = HospitalOrganRequirement.objects.get_or_create(
        hospital=hospital,
        organ_type="Heart",
        blood_type="O+",
        defaults={
            'urgency_level': 'Critical',
            'patient_age': 40,
            'patient_weight': 75.0,
            'patient_height': 180.0,
            'medical_condition': 'Heart failure requiring urgent transplant',
            'is_active': True
        }
    )
    
    print(f"✅ Test data created:")
    print(f"   Hospital: {hospital.hospital_name}")
    print(f"   Donor: {donor.first_name} {donor.last_name}")
    print(f"   Donation: {donation.organ_type} - {donation.blood_type}")
    print(f"   Requirement: {requirement.organ_type} - {requirement.blood_type} ({requirement.urgency_level})")
    
    return hospital, donor, donation, requirement, donor_profile

def test_ml_matching():
    """Test the ML matching system"""
    print("\n🧠 Testing ML Matching System...")
    
    # Create test data
    hospital, donor, donation, requirement, donor_profile = create_test_data()
    
    # Initialize ML matcher
    ml_matcher = OrganMatchingML()
    
    # Test individual prediction
    print("\n🔍 Testing individual match prediction...")
    
    donor_data = {
        'blood_type': donation.blood_type,
        'organ_type': donation.organ_type,
        'age': donor_profile.age,
        'weight': donor_profile.weight,
        'smoking_status': donor_profile.smoking_status,
        'alcohol_consumption': donor_profile.alcohol_consumption
    }
    
    hospital_req = {
        'blood_type': requirement.blood_type,
        'organ_type': requirement.organ_type,
        'urgency_level': requirement.urgency_level,
        'patient_age': requirement.patient_age,
        'patient_weight': requirement.patient_weight
    }
    
    try:
        prediction, probability = ml_matcher.predict_match(donor_data, hospital_req)
        compatibility_score = ml_matcher.calculate_compatibility_score(donor_data, hospital_req)
        
        print(f"📊 Match Results:")
        print(f"   Donor: {donor_data['organ_type']} - {donor_data['blood_type']}")
        print(f"   Hospital: {hospital_req['organ_type']} - {hospital_req['blood_type']} ({hospital_req['urgency_level']})")
        print(f"   ML Prediction: {'✅ MATCH' if prediction == 1 else '❌ NO MATCH'}")
        print(f"   ML Probability: {probability:.3f}")
        print(f"   Compatibility Score: {compatibility_score}%")
        
    except Exception as e:
        print(f"❌ Error in individual prediction: {e}")
        import traceback
        traceback.print_exc()
    
    # Test batch matching
    print("\n🔍 Testing batch matching...")
    
    try:
        matches = ml_matcher.find_matches()
        print(f"📋 Found {len(matches)} potential matches:")
        
        for i, match in enumerate(matches[:3], 1):  # Show first 3 matches
            print(f"   {i}. {match['donor'].first_name} {match['donor'].last_name} → {match['hospital'].hospital_name}")
            print(f"      {match['donation_request'].organ_type} - {match['donation_request'].blood_type}")
            print(f"      Compatibility: {match['compatibility_score']}%, ML Prob: {match['ml_probability']:.3f}")
            print(f"      Urgency: {match['urgency']}")
            print()
        
        if len(matches) > 3:
            print(f"   ... and {len(matches) - 3} more matches")
            
    except Exception as e:
        print(f"❌ Error in batch matching: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("🚀 ML Organ Matching Test Suite")
    print("=" * 50)
    
    # Test the ML matching system
    test_ml_matching()
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    main()