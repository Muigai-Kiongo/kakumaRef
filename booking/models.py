from django.db import models

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
    arrival_date = models.DateField()
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

class LostIDReport(models.Model):
    STATUS_CHOICES = [
        ('R', 'Reported'),
        ('S', 'Resolved'),
    ]
    refugee = models.ForeignKey(Refugee, on_delete=models.CASCADE, related_name='lost_id_reports')
    lost_date = models.DateField()
    report_date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='R')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lost ID report for {self.refugee.full_name} on {self.lost_date}"

