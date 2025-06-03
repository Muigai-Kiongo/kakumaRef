from django.shortcuts import render, redirect
from .models import Refugee, BirthCertificateBooking, LostIDReport
from .forms import RefugeeRegistrationForm, BirthCertificateBookingForm, LostIDReportForm

def public_dashboard(request):
    
    context ={

    }

    return render(request, 'base.html', context)


def register_refugee(request):
    if request.method == 'POST':
        form = RefugeeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = RefugeeRegistrationForm()
    return render(request, 'public_register.html', {'form': form})

def book_birth_certificate(request):
    if request.method == 'POST':
        form = BirthCertificateBookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = BirthCertificateBookingForm()
    return render(request, 'public_booking.html', {'form': form})

def report_lost_id(request):
    if request.method == 'POST':
        form = LostIDReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = LostIDReportForm()
    return render(request, 'public_report_lost_id.html', {'form': form})


