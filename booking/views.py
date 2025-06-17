from django.shortcuts import render, redirect
from .models import Refugee, BirthCertificateBooking, LostDocumentsReport
from .forms import (RefugeeForm, BirthCertificateBookingForm, LostDocumentsReportForm,
                    LostIDDetailsForm, ManifestDetailsForm)

def public_dashboard(request):
    total_refugees = Refugee.objects.count()
    total_bookings = BirthCertificateBooking.objects.count()
    total_lost_reports = LostDocumentsReport.objects.count()
    recent_bookings = BirthCertificateBooking.objects.select_related('refugee').order_by('-booking_date')[:5]

    context = {
        'total_refugees': total_refugees,
        'total_bookings': total_bookings,
        'total_lost_reports': total_lost_reports,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'base.html', context)

def register_refugee(request):
    if request.method == 'POST':
        form = RefugeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RefugeeForm()
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

def report_lost_documents(request):
    if request.method == 'POST':
        report_form = LostDocumentsReportForm(request.POST)
        id_form = LostIDDetailsForm(request.POST) if request.POST.get('document_type') == 'ID' else LostIDDetailsForm()
        manifest_form = ManifestDetailsForm(request.POST) if request.POST.get('document_type') == 'MANIFEST' else ManifestDetailsForm()

        if report_form.is_valid():
            lost_document_report = report_form.save(commit=False)
            lost_document_report.status = 'R'  # Set status to reported
            lost_document_report.save()

            if lost_document_report.document_type == 'ID':
                if id_form.is_valid():
                    id_details = id_form.save(commit=False)
                    id_details.lost_document_report = lost_document_report
                    id_details.save()
                else:
                    return render(request, 'public_report_lost_documents.html', {
                        'report_form': report_form,
                        'id_form': id_form,
                        'manifest_form': manifest_form,
                    })

            elif lost_document_report.document_type == 'MANIFEST':
                if manifest_form.is_valid():
                    manifest_details = manifest_form.save(commit=False)
                    manifest_details.lost_document_report = lost_document_report
                    manifest_details.save()
                else:
                    return render(request, 'public_report_lost_documents.html', {
                        'report_form': report_form,
                        'id_form': id_form,
                        'manifest_form': manifest_form,
                    })

            return redirect('home')  # Redirect after successful submission

    else:
        report_form = LostDocumentsReportForm()
        id_form = LostIDDetailsForm()
        manifest_form = ManifestDetailsForm()

    return render(request, 'public_report_lost_documents.html', {
        'report_form': report_form,
        'id_form': id_form,
        'manifest_form': manifest_form,
    })



def view_registrations(request):
    registrations = Refugee.objects.order_by('-registration_date')
    return render(request, 'view_registrations.html', {'registrations': registrations})

def view_bookings(request):
    bookings = BirthCertificateBooking.objects.select_related('refugee').order_by('-booking_date')
    return render(request, 'view_bookings.html', {'bookings': bookings})

def view_lost_reports(request):
    lost_reports = LostDocumentsReport.objects.select_related('refugee').order_by('-lost_date')
    return render(request, 'view_lost_reports.html', {'lost_reports': lost_reports})
