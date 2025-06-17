from django import forms
from .models import (
    Refugee,
    BirthCertificateBooking,
    LostDocumentsReport,
    LostIDDetails,
    ManifestDetails,
)

class RefugeeForm(forms.ModelForm):
    class Meta:
        model = Refugee
        fields = [
            'full_name',
            'date_of_birth',
            'gender',
            'nationality',
            'arrival_date',
            'contact_info',
            'address',
            'notes',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not full_name or full_name.strip() == '':
            raise forms.ValidationError("Full name is required.")
        return full_name

    # Other clean methods remain unchanged...

class BirthCertificateBookingForm(forms.ModelForm):
    class Meta:
        model = BirthCertificateBooking
        fields = ['refugee', 'booking_date', 'status']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['refugee'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        if not self.initial.get('status'):
            self.initial['status'] = 'P'

    # clean methods remain unchanged...

class LostDocumentsReportForm(forms.ModelForm):
    class Meta:
        model = LostDocumentsReport
        fields = [
            'refugee',
            'document_type',
            'lost_date',
            'description',
            'status',
        ]
        widgets = {
            'lost_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    # clean methods remain unchanged...

class LostIDDetailsForm(forms.ModelForm):
    class Meta:
        model = LostIDDetails
        fields = ['id_number']  # do NOT include lost_document_report, assigned in views

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add form-control class to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number')
        if not id_number or id_number.strip() == '':
            raise forms.ValidationError("ID number is required.")
        return id_number

class ManifestDetailsForm(forms.ModelForm):
    class Meta:
        model = ManifestDetails
        fields = ['manifest_number']  # do NOT include lost_document_report, assigned in views

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add form-control class to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_manifest_number(self):
        manifest_number = self.cleaned_data.get('manifest_number')
        if not manifest_number or manifest_number.strip() == '':
            raise forms.ValidationError("Manifest number is required.")
        return manifest_number
