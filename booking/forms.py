from django import forms
from .models import Refugee, BirthCertificateBooking, LostIDReport

class RefugeeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Refugee
        fields = ['full_name', 'date_of_birth', 'gender', 'nationality', 'arrival_date', 'contact_info', 'address', 'notes']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BirthCertificateBookingForm(forms.ModelForm):
    class Meta:
        model = BirthCertificateBooking
        fields = ['refugee', 'booking_date']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'refugee': forms.Select(attrs={'class': 'form-control'}),
        }

class LostIDReportForm(forms.ModelForm):
    class Meta:
        model = LostIDReport
        fields = ['refugee', 'lost_date', 'description']
        widgets = {
            'lost_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'refugee': forms.Select(attrs={'class': 'form-control'}),
        }
