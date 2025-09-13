from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import HospitalOrganRequirement, DonorMedicalProfile
from .matching_algorithm import OrganMatchingML
from donors.models import DonationRequests
import json

@login_required
def hospital_requirements(request):
    """View for hospitals to add organ requirements"""
    if not request.user.is_staff:
        return redirect('donor-home')
    
    if request.method == 'POST':
        requirement = HospitalOrganRequirement.objects.create(
            hospital=request.user,
            organ_type=request.POST['organ_type'],
            blood_type=request.POST['blood_type'],
            urgency_level=request.POST['urgency_level'],
            patient_age=int(request.POST['patient_age']),
            patient_weight=float(request.POST['patient_weight']),
            patient_height=float(request.POST['patient_height']),
            medical_condition=request.POST['medical_condition']
        )
        messages.success(request, 'Organ requirement added successfully!')
        return redirect('hospital_requirements')
    
    requirements = HospitalOrganRequirement.objects.filter(hospital=request.user, is_active=True)
    return render(request, 'ml_matching/hospital_requirements.html', {'requirements': requirements})

@login_required
def donor_medical_profile(request):
    """View for donors to add/update medical profile"""
    if request.user.is_staff:
        return redirect('hospital-main-page')
    
    try:
        profile = DonorMedicalProfile.objects.get(donor=request.user)
    except DonorMedicalProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        if profile:
            profile.age = int(request.POST['age'])
            profile.weight = float(request.POST['weight'])
            profile.height = float(request.POST['height'])
            profile.blood_type = request.POST['blood_type']
            profile.medical_history = request.POST['medical_history']
            profile.smoking_status = request.POST.get('smoking_status') == 'on'
            profile.alcohol_consumption = request.POST.get('alcohol_consumption') == 'on'
            profile.chronic_diseases = request.POST['chronic_diseases']
            profile.medications = request.POST['medications']
            profile.save()
        else:
            profile = DonorMedicalProfile.objects.create(
                donor=request.user,
                age=int(request.POST['age']),
                weight=float(request.POST['weight']),
                height=float(request.POST['height']),
                blood_type=request.POST['blood_type'],
                medical_history=request.POST['medical_history'],
                smoking_status=request.POST.get('smoking_status') == 'on',
                alcohol_consumption=request.POST.get('alcohol_consumption') == 'on',
                chronic_diseases=request.POST['chronic_diseases'],
                medications=request.POST['medications']
            )
        
        messages.success(request, 'Medical profile updated successfully!')
        return redirect('donor_medical_profile')
    
    return render(request, 'ml_matching/donor_medical_profile.html', {'profile': profile})

@login_required
def ml_matches(request):
    """View to show ML-based matches"""
    if not request.user.is_staff:
        return redirect('donor-home')
    
    ml_matcher = OrganMatchingML()
    matches = ml_matcher.find_matches()
    
    # Filter matches for current hospital
    hospital_matches = [match for match in matches if match['hospital'] == request.user]
    
    return render(request, 'ml_matching/ml_matches.html', {'matches': hospital_matches})

@login_required
def train_model_view(request):
    """View to train the ML model"""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    if request.method == 'POST':
        ml_matcher = OrganMatchingML()
        accuracy = ml_matcher.train_model()
        return JsonResponse({'success': True, 'accuracy': accuracy})
    
    return render(request, 'ml_matching/train_model.html')

def api_find_matches(request):
    """API endpoint to find matches"""
    if request.method == 'GET':
        ml_matcher = OrganMatchingML()
        matches = ml_matcher.find_matches()
        
        # Convert to JSON serializable format
        matches_data = []
        for match in matches:
            matches_data.append({
                'donor_name': f"{match['donor'].first_name} {match['donor'].last_name}",
                'donor_blood_type': match['donation_request'].blood_type,
                'organ_type': match['donation_request'].organ_type,
                'hospital_name': match['hospital'].hospital_name,
                'urgency': match['urgency'],
                'compatibility_score': match['compatibility_score'],
                'ml_probability': float(match['ml_probability'])
            })
        
        return JsonResponse({'matches': matches_data})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)