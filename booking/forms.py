from django import forms
from .models import Refugee, BirthCertificateBooking, LostIDReport

class RefugeeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Refugee
        fields = ['full_name', 'date_of_birth', 'gender', 'nationality', 'arrival_date', 'contact_info', 'address', 'notes']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(),
            'notes': forms.Textarea(attrs={'rows':3}),
            'address': forms.Textarea(attrs={'rows':2}),
        }

class BirthCertificateBookingForm(forms.ModelForm):
    class Meta:
        model = BirthCertificateBooking
        fields = ['refugee', 'booking_date']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
        }

class LostIDReportForm(forms.ModelForm):
    class Meta:
        model = LostIDReport
        fields = ['refugee', 'lost_date', 'description']
        widgets = {
            'lost_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows':3}),
        }

