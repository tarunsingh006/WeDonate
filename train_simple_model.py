"""
Simple ML training script with synthetic data (no CSV dependency)
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, RobustScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_selection import SelectKBest, f_classif
import joblib
import os

def generate_high_quality_data():
    """Generate high-quality synthetic organ donation data"""
    np.random.seed(42)
    n_samples = 2000
    
    organ_types = ['Heart', 'Liver', 'Kidney', 'Lung', 'Pancreas']
    blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    urgency_levels = ['Critical', 'Urgent', 'High', 'Medium', 'Low']
    
    # Blood compatibility matrix
    compatibility_matrix = {
        'O-': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'],
        'O+': ['O+', 'A+', 'B+', 'AB+'],
        'A-': ['A-', 'A+', 'AB-', 'AB+'],
        'A+': ['A+', 'AB+'],
        'B-': ['B-', 'B+', 'AB-', 'AB+'],
        'B+': ['B+', 'AB+'],
        'AB-': ['AB-', 'AB+'],
        'AB+': ['AB+']
    }
    
    def blood_compatible(donor, recipient):
        return recipient in compatibility_matrix.get(donor, [])
    
    def calculate_score(donor_blood, recipient_blood, organ_match, age_diff, weight_ratio, health):
        score = 0
        if blood_compatible(donor_blood, recipient_blood):
            score += 35 if donor_blood == recipient_blood else 30
        if organ_match:
            score += 25
        if age_diff <= 5:
            score += 20
        elif age_diff <= 10:
            score += 16
        elif age_diff <= 15:
            score += 12
        elif age_diff <= 20:
            score += 8
        if weight_ratio >= 0.9:
            score += 10
        elif weight_ratio >= 0.8:
            score += 8
        elif weight_ratio >= 0.7:
            score += 5
        score += health * 5
        return min(score, 100)
    
    data = []
    for _ in range(n_samples):
        # Generate donor and recipient data
        donor_blood = np.random.choice(blood_types)
        recipient_blood = np.random.choice(blood_types)
        organ_type = np.random.choice(organ_types)
        urgency = np.random.choice(urgency_levels)
        
        donor_age = np.random.randint(18, 70)
        recipient_age = np.random.randint(18, 80)
        donor_weight = np.random.normal(70, 15)
        recipient_weight = np.random.normal(70, 15)
        
        smoking = np.random.choice([0, 1], p=[0.8, 0.2])
        alcohol = np.random.choice([0, 1], p=[0.7, 0.3])
        
        # Calculate features
        age_diff = abs(donor_age - recipient_age)
        weight_ratio = min(donor_weight, recipient_weight) / max(donor_weight, recipient_weight)
        organ_match = 1
        health_score = 2 - smoking - alcohol
        
        compatibility_score = calculate_score(
            donor_blood, recipient_blood, organ_match, age_diff, weight_ratio, health_score
        )
        
        # Create realistic match probability based on compatibility
        match_prob = compatibility_score / 100.0
        # Add some noise and bias towards higher compatibility
        match_prob = match_prob * 0.8 + 0.1
        match = 1 if np.random.random() < match_prob else 0
        
        data.append([
            donor_blood, recipient_blood, organ_type, urgency,
            donor_age, recipient_age, donor_weight, recipient_weight,
            smoking, alcohol, compatibility_score, age_diff, weight_ratio,
            organ_match, health_score, match
        ])
    
    columns = [
        'donor_blood', 'recipient_blood', 'organ_type', 'urgency',
        'donor_age', 'recipient_age', 'donor_weight', 'recipient_weight',
        'smoking', 'alcohol', 'compatibility_score', 'age_diff', 'weight_ratio',
        'organ_match', 'health_score', 'match'
    ]
    
    return pd.DataFrame(data, columns=columns)

def train_high_accuracy_model():
    """Train ensemble model for 90%+ accuracy"""
    print("🧠 Generating high-quality training data...")
    df = generate_high_quality_data()
    print(f"📊 Generated {len(df)} training samples")
    
    # Encode categorical variables
    label_encoders = {}
    categorical_cols = ['donor_blood', 'recipient_blood', 'organ_type', 'urgency']
    for col in categorical_cols:
        le = LabelEncoder()
        df[col + '_encoded'] = le.fit_transform(df[col])
        label_encoders[col] = le
    
    # Prepare features
    feature_cols = [
        'donor_blood_encoded', 'recipient_blood_encoded', 'organ_type_encoded',
        'urgency_encoded', 'donor_age', 'recipient_age', 'donor_weight',
        'recipient_weight', 'smoking', 'alcohol', 'compatibility_score',
        'age_diff', 'weight_ratio', 'organ_match', 'health_score'
    ]
    
    X = df[feature_cols]
    y = df['match']
    
    print(f"🎯 Target distribution: {y.value_counts().to_dict()}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Feature selection
    selector = SelectKBest(f_classif, k=12)
    X_train_selected = selector.fit_transform(X_train_scaled, y_train)
    X_test_selected = selector.transform(X_test_scaled)
    
    # Create ensemble model
    rf = RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_split=5, random_state=42)
    gb = GradientBoostingClassifier(n_estimators=150, learning_rate=0.1, max_depth=8, random_state=42)
    svm = SVC(kernel='rbf', C=10, gamma='scale', probability=True, random_state=42)
    mlp = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
    
    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('gb', gb), ('svm', svm), ('mlp', mlp)],
        voting='soft'
    )
    
    # Cross-validation
    print("🔄 Performing cross-validation...")
    cv_scores = cross_val_score(ensemble, X_train_selected, y_train, cv=5, scoring='accuracy')
    print(f"Cross-validation scores: {cv_scores}")
    print(f"Mean CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Train final model
    print("🚀 Training ensemble model...")
    ensemble.fit(X_train_selected, y_train)
    
    # Evaluate
    y_pred = ensemble.predict(X_test_selected)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n🎉 Training Results:")
    print(f"   Final Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    if accuracy >= 0.90:
        print("   ✅ TARGET ACHIEVED: 90%+ accuracy!")
    elif accuracy >= 0.85:
        print("   🟡 Good performance: 85%+ accuracy")
    else:
        print("   🔴 Below target: Consider more data or feature engineering")
    
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    os.makedirs('ml_matching', exist_ok=True)
    joblib.dump(ensemble, 'ml_matching/trained_model.joblib')
    joblib.dump(scaler, 'ml_matching/scaler.joblib')
    joblib.dump(label_encoders, 'ml_matching/encoders.joblib')
    joblib.dump(selector, 'ml_matching/feature_selector.joblib')
    
    print(f"\n📁 Model saved successfully!")
    return accuracy

def test_model():
    """Test the trained model with sample cases"""
    print("\n🧪 Testing trained model...")
    
    # Load model components
    ensemble = joblib.load('ml_matching/trained_model.joblib')
    scaler = joblib.load('ml_matching/scaler.joblib')
    encoders = joblib.load('ml_matching/encoders.joblib')
    selector = joblib.load('ml_matching/feature_selector.joblib')
    
    # Test cases
    test_cases = [
        {
            'name': 'Perfect Match',
            'data': [0, 0, 0, 0, 35, 35, 70, 70, 0, 0, 95, 0, 1.0, 1, 2]  # Perfect compatibility
        },
        {
            'name': 'Good Match',
            'data': [1, 2, 1, 1, 30, 35, 65, 70, 0, 0, 85, 5, 0.93, 1, 2]  # Good compatibility
        },
        {
            'name': 'Poor Match',
            'data': [3, 7, 2, 4, 25, 60, 60, 90, 1, 1, 25, 35, 0.67, 1, 0]  # Poor compatibility
        }
    ]
    
    for case in test_cases:
        input_data = np.array([case['data']])
        input_scaled = scaler.transform(input_data)
        input_selected = selector.transform(input_scaled)
        
        prediction = ensemble.predict(input_selected)[0]
        probability = ensemble.predict_proba(input_selected)[0][1]
        
        print(f"   {case['name']}: {'✅ MATCH' if prediction == 1 else '❌ NO MATCH'} (Prob: {probability:.3f})")

def main():
    print("🚀 High-Accuracy ML Model Training (Synthetic Data)")
    print("=" * 60)
    
    try:
        accuracy = train_high_accuracy_model()
        test_model()
        
        print(f"\n🎯 Summary:")
        print(f"   - Model Accuracy: {accuracy*100:.2f}%")
        print(f"   - Algorithm: Ensemble (RF + GB + SVM + MLP)")
        print(f"   - Features: 15 engineered features")
        print(f"   - Data: 2000 synthetic samples")
        print(f"   - Files: ml_matching/*.joblib")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()