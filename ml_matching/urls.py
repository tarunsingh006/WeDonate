from django.urls import path
from . import views

urlpatterns = [
    path('hospital-requirements/', views.hospital_requirements, name='hospital_requirements'),
    path('donor-medical-profile/', views.donor_medical_profile, name='donor_medical_profile'),
    path('ml-matches/', views.ml_matches, name='ml_matches'),
    path('train-model/', views.train_model_view, name='train_model'),
    path('api/matches/', views.api_find_matches, name='api_matches'),
]