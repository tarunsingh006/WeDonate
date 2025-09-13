"""
Standalone ML training script that doesn't require Django setup
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, RobustScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.feature_selection import SelectKBest, f_classif
import joblib
import os

class StandaloneOrganMatchingML:
    def __init__(self):
        # Ensemble of high-performance models
        rf = RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_split=5, random_state=42)
        gb = GradientBoostingClassifier(n_estimators=150, learning_rate=0.1, max_depth=8, random_state=42)
        svm = SVC(kernel='rbf', C=10, gamma='scale', probability=True, random_state=42)
        mlp = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
        
        self.model = VotingClassifier(
            estimators=[('rf', rf), ('gb', gb), ('svm', svm), ('mlp', mlp)],
            voting='soft'
        )
        self.scaler = RobustScaler()
        self.feature_selector = SelectKBest(f_classif, k=10)
        self.label_encoders = {}
        
    def blood_compatibility(self, donor_blood, recipient_blood):
        """Check blood type compatibility"""
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
        return recipient_blood in compatibility_matrix.get(donor_blood, [])
    
    def calculate_compatibility_score(self, donor_data, hospital_req):
        """Enhanced compatibility score with medical precision"""
        score = 0
        
        # Blood type compatibility (35% weight)
        if self.blood_compatibility(donor_data['blood_type'], hospital_req['blood_type']):
            if donor_data['blood_type'] == hospital_req['blood_type']:
                score += 35
            else:
                score += 30
        
        # Organ type match (25% weight)
        if donor_data['organ_type'] == hospital_req['organ_type']:
            score += 25
        
        # Age compatibility (20% weight)
        age_diff = abs(donor_data['age'] - hospital_req['patient_age'])
        if age_diff <= 5:
            score += 20
        elif age_diff <= 10:
            score += 16
        elif age_diff <= 15:
            score += 12
        elif age_diff <= 20:
            score += 8
        elif age_diff <= 30:
            score += 4
        
        # Weight compatibility (10% weight)
        weight_ratio = min(donor_data['weight'], hospital_req['patient_weight']) / max(donor_data['weight'], hospital_req['patient_weight'])
        if weight_ratio >= 0.9:
            score += 10
        elif weight_ratio >= 0.8:
            score += 8
        elif weight_ratio >= 0.7:
            score += 5
        elif weight_ratio >= 0.6:
            score += 2
        
        # Medical condition compatibility (10% weight)
        health_score = 0
        if not donor_data['smoking_status']:
            health_score += 5
        if not donor_data['alcohol_consumption']:
            health_score += 5
        score += health_score
        
        return min(score, 100)
    
    def prepare_training_data(self):
        """Load and prepare training data from CSV file"""
        try:
            csv_path = os.path.join('ml_matching', 'Organ Donation.csv')
            # Try multiple CSV reading strategies
            try:
                df = pd.read_csv(csv_path, encoding='utf-8', on_bad_lines='skip')
            except:
                try:
                    df = pd.read_csv(csv_path, encoding='latin-1', on_bad_lines='skip')
                except:
                    df = pd.read_csv(csv_path, encoding='cp1252', on_bad_lines='skip')
            
            print(f"Successfully loaded {len(df)} records from CSV")
            
            data = []
            
            for _, row in df.iterrows():
                # Extract age from age range
                age_str = str(row.get('Age', '18-25 years'))
                if '18-25' in age_str:
                    age = 22
                elif '26-40' in age_str:
                    age = 33
                elif '41-55' in age_str:
                    age = 48
                else:
                    age = 60
                
                # Determine willingness to donate
                willing_to_donate = 1 if str(row.get('Are you willing to donate organs?', 'No')).lower() == 'yes' else 0
                
                # Generate synthetic organ and blood type data
                np.random.seed(hash(str(row.get('Name', 'Unknown'))) % 2**32)
                organ_types = ['Heart', 'Liver', 'Kidney', 'Lung', 'Pancreas']
                blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
                urgency_levels = ['Critical', 'Urgent', 'High', 'Medium', 'Low']
                
                donor_blood = np.random.choice(blood_types)
                recipient_blood = np.random.choice(blood_types)
                organ_type = np.random.choice(organ_types)
                urgency = np.random.choice(urgency_levels)
                
                # Estimate weight based on gender
                gender = str(row.get('Gender', 'Male'))
                if gender.lower() == 'male':
                    weight = np.random.normal(75, 12)
                else:
                    weight = np.random.normal(65, 10)
                
                recipient_age = age + np.random.randint(-10, 10)
                recipient_weight = weight + np.random.normal(0, 8)
                
                smoking = 0
                alcohol = 0
                
                # Calculate compatibility score
                temp_donor = {
                    'blood_type': donor_blood,
                    'organ_type': organ_type,
                    'age': age,
                    'weight': weight,
                    'smoking_status': smoking,
                    'alcohol_consumption': alcohol
                }
                temp_req = {
                    'blood_type': recipient_blood,
                    'organ_type': organ_type,
                    'patient_age': recipient_age,
                    'patient_weight': recipient_weight
                }
                
                compatibility_score = self.calculate_compatibility_score(temp_donor, temp_req)
                match = willing_to_donate
                
                data.append([
                    donor_blood, recipient_blood, organ_type, urgency,
                    age, recipient_age, weight, recipient_weight,
                    smoking, alcohol, compatibility_score, match
                ])
            
            columns = [
                'donor_blood', 'recipient_blood', 'organ_type', 'urgency',
                'donor_age', 'recipient_age', 'donor_weight', 'recipient_weight',
                'smoking', 'alcohol', 'compatibility_score', 'match'
            ]
            
            return pd.DataFrame(data, columns=columns)
            
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            return self._generate_synthetic_data()
    
    def _generate_synthetic_data(self):
        """Generate synthetic training data as fallback"""
        np.random.seed(42)
        n_samples = 1000
        
        organ_types = ['Heart', 'Liver', 'Kidney', 'Lung', 'Pancreas']
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        urgency_levels = ['Critical', 'Urgent', 'High', 'Medium', 'Low']
        
        data = []
        for _ in range(n_samples):
            donor_blood = np.random.choice(blood_types)
            recipient_blood = np.random.choice(blood_types)
            organ_type = np.random.choice(organ_types)
            urgency = np.random.choice(urgency_levels)
            
            donor_age = np.random.randint(18, 70)
            recipient_age = np.random.randint(18, 80)
            donor_weight = np.random.normal(70, 15)
            recipient_weight = np.random.normal(70, 15)
            
            smoking = np.random.choice([0, 1], p=[0.7, 0.3])
            alcohol = np.random.choice([0, 1], p=[0.6, 0.4])
            
            temp_donor = {
                'blood_type': donor_blood,
                'organ_type': organ_type,
                'age': donor_age,
                'weight': donor_weight,
                'smoking_status': smoking,
                'alcohol_consumption': alcohol
            }
            temp_req = {
                'blood_type': recipient_blood,
                'organ_type': organ_type,
                'patient_age': recipient_age,
                'patient_weight': recipient_weight
            }
            
            compatibility_score = self.calculate_compatibility_score(temp_donor, temp_req)
            match = 1 if compatibility_score >= 70 else 0
            
            data.append([
                donor_blood, recipient_blood, organ_type, urgency,
                donor_age, recipient_age, donor_weight, recipient_weight,
                smoking, alcohol, compatibility_score, match
            ])
        
        columns = [
            'donor_blood', 'recipient_blood', 'organ_type', 'urgency',
            'donor_age', 'recipient_age', 'donor_weight', 'recipient_weight',
            'smoking', 'alcohol', 'compatibility_score', 'match'
        ]
        
        return pd.DataFrame(data, columns=columns)
    
    def train_model(self):
        """Train advanced ensemble model for 90%+ accuracy"""
        df = self.prepare_training_data()
        
        # Enhanced feature engineering
        categorical_cols = ['donor_blood', 'recipient_blood', 'organ_type', 'urgency']
        for col in categorical_cols:
            le = LabelEncoder()
            df[col + '_encoded'] = le.fit_transform(df[col])
            self.label_encoders[col] = le
        
        # Create additional engineered features
        df['age_diff'] = abs(df['donor_age'] - df['recipient_age'])
        df['weight_ratio'] = df['donor_weight'] / df['recipient_weight']
        df['blood_exact_match'] = (df['donor_blood'] == df['recipient_blood']).astype(int)
        df['health_score'] = (2 - df['smoking'] - df['alcohol'])
        df['urgency_weight'] = df['urgency_encoded'] * 0.2
        
        # Prepare enhanced features
        feature_cols = [
            'donor_blood_encoded', 'recipient_blood_encoded', 'organ_type_encoded',
            'urgency_encoded', 'donor_age', 'recipient_age', 'donor_weight',
            'recipient_weight', 'smoking', 'alcohol', 'compatibility_score',
            'age_diff', 'weight_ratio', 'blood_exact_match', 'health_score', 'urgency_weight'
        ]
        
        X = df[feature_cols]
        y = df['match']
        
        # Handle class imbalance with stratified split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Feature selection
        X_train_selected = self.feature_selector.fit_transform(X_train_scaled, y_train)
        X_test_selected = self.feature_selector.transform(X_test_scaled)
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train_selected, y_train, cv=5, scoring='accuracy')
        print(f"Cross-validation scores: {cv_scores}")
        print(f"Mean CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        # Train ensemble model
        self.model.fit(X_train_selected, y_train)
        
        # Evaluate on test set
        y_pred = self.model.predict(X_test_selected)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Test Accuracy: {accuracy:.4f}")
        print(f"Classification Report:")
        print(classification_report(y_test, y_pred))
        
        # Save model components
        os.makedirs('ml_matching', exist_ok=True)
        joblib.dump(self.model, 'ml_matching/trained_model.joblib')
        joblib.dump(self.scaler, 'ml_matching/scaler.joblib')
        joblib.dump(self.label_encoders, 'ml_matching/encoders.joblib')
        joblib.dump(self.feature_selector, 'ml_matching/feature_selector.joblib')
        
        return accuracy

def main():
    print("🚀 Training High-Accuracy ML Model (Standalone Version)")
    print("=" * 60)
    
    # Check if CSV file exists
    csv_path = os.path.join('ml_matching', 'Organ Donation.csv')
    if os.path.exists(csv_path):
        print(f"✅ Found CSV file: {csv_path}")
        df = pd.read_csv(csv_path)
        print(f"📊 Dataset loaded: {len(df)} records")
    else:
        print(f"⚠️  CSV file not found, using synthetic data")
    
    # Initialize and train the model
    ml_matcher = StandaloneOrganMatchingML()
    
    print(f"\n🧠 Training Advanced Ensemble Model...")
    print("   - Random Forest (200 trees)")
    print("   - Gradient Boosting (150 estimators)")
    print("   - Support Vector Machine (RBF kernel)")
    print("   - Neural Network (100-50 hidden layers)")
    
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
        
        print(f"\n📁 Model files saved in: ml_matching/")
        print("   - trained_model.joblib")
        print("   - scaler.joblib")
        print("   - encoders.joblib")
        print("   - feature_selector.joblib")
        
    except Exception as e:
        print(f"❌ Error during training: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()