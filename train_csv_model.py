import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organ_donation.settings')
django.setup()

from ml_matching.matching_algorithm import OrganMatchingML
import pandas as pd

def main():
    print("🚀 Training ML Model with Organ Donation CSV Data...")
    
    # Initialize the ML matcher
    ml_matcher = OrganMatchingML()
    
    # Check if CSV file exists
    csv_path = os.path.join('ml_matching', 'Organ Donation.csv')
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found at: {csv_path}")
        print("Please ensure 'Organ Donation.csv' is in the ml_matching folder")
        return
    
    print(f"✅ Found CSV file: {csv_path}")
    
    # Load and preview the data
    try:
        df = pd.read_csv(csv_path)
        print(f"📊 Dataset loaded: {len(df)} records")
        print(f"📋 Columns: {list(df.columns)[:5]}...")  # Show first 5 columns
        
        # Check willingness to donate distribution
        willing_col = 'Are you willing to donate organs?'
        if willing_col in df.columns:
            willing_counts = df[willing_col].value_counts()
            print(f"🎯 Donation willingness distribution:")
            for value, count in willing_counts.items():
                print(f"   {value}: {count} ({count/len(df)*100:.1f}%)")
        
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return
    
    # Train the model
    print("\n🧠 Training the model...")
    try:
        accuracy = ml_matcher.train_model()
        print(f"✅ Model trained successfully!")
        print(f"🎯 Accuracy: {accuracy:.2f}")
        
        # Test the model with sample data
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
        
        print(f"📋 Test Case:")
        print(f"   Donor: {donor_data['organ_type']} - {donor_data['blood_type']}, Age {donor_data['age']}")
        print(f"   Hospital: {hospital_req['organ_type']} - {hospital_req['blood_type']}, {hospital_req['urgency_level']}")
        print(f"   Result: {'✅ MATCH' if prediction == 1 else '❌ NO MATCH'}")
        print(f"   ML Probability: {probability:.3f}")
        print(f"   Compatibility Score: {compatibility_score}%")
        
        print(f"\n🎉 Model training completed successfully!")
        print(f"📁 Model files saved in: ml_matching/")
        
    except Exception as e:
        print(f"❌ Error during training: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()