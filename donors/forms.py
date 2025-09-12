from django import forms
from .models import Appointments, DonationRequests
from hospitals.models import User
from datetime import datetime, timedelta

class AppointmentForm(forms.ModelForm):
    TIME_CHOICES = [
        ('08:00 - 09:00', '08:00 - 09:00 AM'),
        ('09:00 - 10:00', '09:00 - 10:00 AM'),
        ('10:00 - 11:00', '10:00 - 11:00 AM'),
        ('11:00 - 12:00', '11:00 - 12:00 PM'),
        ('12:00 - 13:00', '12:00 - 01:00 PM'),
        ('13:00 - 14:00', '01:00 - 02:00 PM'),
        ('14:00 - 15:00', '02:00 - 03:00 PM'),
        ('15:00 - 16:00', '03:00 - 04:00 PM'),
        ('16:00 - 17:00', '04:00 - 05:00 PM'),
        ('17:00 - 18:00', '05:00 - 06:00 PM'),
    ]
    
    donation_request = forms.ModelChoiceField(
        queryset=DonationRequests.objects.none(),
        empty_label="Choose your donation request",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        })
    )
    
    hospital = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),
        empty_label="Choose a hospital",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        })
    )
    
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': datetime.now().date(),
            'max': (datetime.now().date() + timedelta(days=90)),
            'required': True
        })
    )
    
    time = forms.ChoiceField(
        choices=TIME_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        })
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any special requirements or notes for the hospital...'
        })
    )
    
    class Meta:
        model = Appointments
        fields = ['donation_request', 'hospital', 'date', 'time', 'notes']
    
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Only show approved donation requests for the current user
            self.fields['donation_request'].queryset = DonationRequests.objects.filter(
                donor=user, 
                donation_status='Approved'
            )
            
            # Customize the display of donation requests
            self.fields['donation_request'].label_from_instance = lambda obj: f"#DON{obj.id} - {obj.organ_type} ({obj.blood_type})"
            
            # Customize the display of hospitals
            self.fields['hospital'].label_from_instance = lambda obj: f"{obj.hospital_name or obj.username} - {obj.city}, {obj.province}"
    
    def clean_date(self):
        date = self.cleaned_data['date']
        today = datetime.now().date()
        max_date = today + timedelta(days=90)
        
        if date < today:
            raise forms.ValidationError("Appointment date cannot be in the past.")
        
        if date > max_date:
            raise forms.ValidationError("Appointment date cannot be more than 3 months in the future.")
        
        return date