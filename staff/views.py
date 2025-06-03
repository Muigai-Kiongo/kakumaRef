from django.shortcuts import render, redirect
from booking.models import Refugee, BirthCertificateBooking, LostIDReport
from booking.forms import RefugeeRegistrationForm, BirthCertificateBookingForm, LostIDReportForm


def manage_dashboard(request):
    return render(request, 'manage_dashboard.html')

def manage_refugees(request):
    refugees = Refugee.objects.all()
    return render(request, 'manage_refugees.html', {'refugees': refugees})

def manage_bookings(request):
    bookings = BirthCertificateBooking.objects.all()
    return render(request, 'manage_bookings.html', {'bookings': bookings})

def manage_reports(request):
    reports = LostIDReport.objects.all()
    return render(request, 'manage_lost_ids.html', {'reports': reports})
