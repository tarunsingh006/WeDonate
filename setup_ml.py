import os
import django
import subprocess
import sys

def install_requirements():
    """Install ML requirements"""
    print("Installing ML dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_ml.txt"])

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organ_donation.settings')
    django.setup()

def create_migrations():
    """Create and run migrations for ML models"""
    print("Creating migrations...")
    os.system('python manage.py makemigrations ml_matching')
    print("Running migrations...")
    os.system('python manage.py migrate')

def train_model():
    """Train the ML model"""
    print("Training ML model...")
    from ml_matching.matching_algorithm import OrganMatchingML
    
    ml_matcher = OrganMatchingML()
    accuracy = ml_matcher.train_model()
    print(f"✅ Model trained with accuracy: {accuracy:.2f}")

def main():
    print("🚀 Setting up ML Organ Matching System...")
    
    try:
        # Install requirements
        install_requirements()
        
        # Setup Django
        setup_django()
        
        # Create migrations
        create_migrations()
        
        # Train model
        train_model()
        
        print("\n✅ ML Organ Matching System setup complete!")
        print("\nNext steps:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: /ml-matching/hospital-requirements/ (for hospitals)")
        print("3. Visit: /ml-matching/donor-medical-profile/ (for donors)")
        print("4. Visit: /ml-matching/ml-matches/ (to see matches)")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()