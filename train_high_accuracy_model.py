import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organ_donation.settings')
django.setup()

from ml_matching.matching_algorithm import OrganMatchingML
import pandas as pd
import numpy as np

def main():
    print("🚀 Training High-Accuracy ML Model (Target: 90%+)")
    print("=" * 60)
    
    # Initialize the advanced ML matcher
    ml_matcher = OrganMatchingML()
    
    # Check if CSV file exists
    csv_path = os.path.join('ml_matching', 'Organ Donation.csv')
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found at: {csv_path}")
        print("Please ensure 'Organ Donation.csv' is in the ml_matching folder")
        return
    
    print(f"✅ Found CSV file: {csv_path}")
    
    # Load and analyze the data
    try:
        df = pd.read_csv(csv_path)
        print(f"📊 Dataset loaded: {len(df)} records")
        
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
    
    # Train the advanced ensemble model
    print(f"\n🧠 Training Advanced Ensemble Model...")
    print("   - Random Forest (200 trees)")
    print("   - Gradient Boosting (150 estimators)")
    print("   - Support Vector Machine (RBF kernel)")
    print("   - Neural Network (100-50 hidden layers)")
    print("   - Feature Selection & Engineering")
    print("   - Cross-validation & Hyperparameter tuning")
    
    try:
        accuracy = ml_matcher.train_model()
        
        print(f"\n🎉 Training Results:")
        print(f"   Final Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        
        if accuracy >= 0.90:
            print("   ✅ TARGET ACHIEVED: 90%+ accuracy!")
        elif accuracy >= 0.85:
            print("   🟡 Good performance: 85%+ accuracy")
        else:
            print("   🔴 Below target: Consider more data or feature engineering")
        
        # Test the model with multiple scenarios
        print(f"\n🧪 Testing Model Performance...")
        
        test_cases = [
            {
                'name': 'Perfect Match',
                'donor': {'blood_type': 'O+', 'organ_type': 'Heart', 'age': 35, 'weight': 70.0, 'smoking_status': False, 'alcohol_consumption': False},
                'hospital': {'blood_type': 'O+', 'organ_type': 'Heart', 'urgency_level': 'Critical', 'patient_age': 35, 'patient_weight': 70.0}
            },
            {
                'name': 'Compatible Match',
                'donor': {'blood_type': 'O-', 'organ_type': 'Kidney', 'age': 30, 'weight': 65.0, 'smoking_status': False, 'alcohol_consumption': False},
                'hospital': {'blood_type': 'A+', 'organ_type': 'Kidney', 'urgency_level': 'Urgent', 'patient_age': 35, 'patient_weight': 70.0}
            },
            {
                'name': 'Poor Match',
                'donor': {'blood_type': 'A+', 'organ_type': 'Liver', 'age': 25, 'weight': 60.0, 'smoking_status': True, 'alcohol_consumption': True},
                'hospital': {'blood_type': 'B-', 'organ_type': 'Heart', 'urgency_level': 'Low', 'patient_age': 60, 'patient_weight': 90.0}
            }
        ]
        
        for i, case in enumerate(test_cases, 1):
            prediction, probability = ml_matcher.predict_match(case['donor'], case['hospital'])
            compatibility = ml_matcher.calculate_compatibility_score(case['donor'], case['hospital'])
            
            print(f"\n   Test {i}: {case['name']}")
            print(f"      Prediction: {'✅ MATCH' if prediction == 1 else '❌ NO MATCH'}")
            print(f"      ML Probability: {probability:.3f}")
            print(f"      Compatibility: {compatibility}%")
        
        print(f"\n📁 Model Components Saved:")
        print(f"   - Ensemble Model: ml_matching/trained_model.joblib")
        print(f"   - Feature Scaler: ml_matching/scaler.joblib")
        print(f"   - Label Encoders: ml_matching/encoders.joblib")
        print(f"   - Feature Selector: ml_matching/feature_selector.joblib")
        
        print(f"\n🎯 Model Features:")
        print(f"   - 4 Advanced Algorithms (Voting Ensemble)")
        print(f"   - 16 Engineered Features")
        print(f"   - Robust Scaling & Feature Selection")
        print(f"   - Cross-validation Verified")
        print(f"   - Medical-grade Compatibility Scoring")
        
    except Exception as e:
        print(f"❌ Error during training: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()