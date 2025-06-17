from django.db import models
from django.utils import timezone

class Refugee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=100)
    arrival_date = models.DateField(default=timezone.now)
    registration_date = models.DateField(auto_now_add=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name

class BirthCertificateBooking(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    ]
    refugee = models.ForeignKey(Refugee, on_delete=models.CASCADE, related_name='birth_certificate_bookings')
    booking_date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.refugee.full_name} on {self.booking_date}"

class LostDocumentsReport(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('ID', 'Lost ID'),
        ('MANIFEST', 'Manifest'),
    ]
    STATUS_CHOICES = [
        ('R', 'Reported'),
        ('S', 'Resolved'),
    ]
    refugee = models.ForeignKey(Refugee, on_delete=models.CASCADE, related_name='lost_documents_reports')
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPE_CHOICES)
    lost_date = models.DateField()
    report_date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='R')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} report for {self.refugee.full_name} on {self.lost_date}"

    @property
    def details(self):
        if self.document_type == 'ID':
            return getattr(self, 'id_details', None)
        elif self.document_type == 'MANIFEST':
            return getattr(self, 'manifest_details', None)
        return None

class LostIDDetails(models.Model):
    lost_document_report = models.OneToOneField(LostDocumentsReport, on_delete=models.CASCADE, related_name='id_details')
    id_number = models.CharField(max_length=100)

    def __str__(self):
        return f"ID Details: {self.id_number} for {self.lost_document_report.refugee.full_name}"

class ManifestDetails(models.Model):
    lost_document_report = models.OneToOneField(LostDocumentsReport, on_delete=models.CASCADE, related_name='manifest_details')
    manifest_number = models.CharField(max_length=100)
    # Add other manifest-specific fields here

    def __str__(self):
        return f"Manifest Details: {self.manifest_number} for {self.lost_document_report.refugee.full_name}"

