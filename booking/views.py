from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .utils import filter_by_timeframe  
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
            return redirect('payment')
    else:
        form = BirthCertificateBookingForm()
    return render(request, 'public_booking.html', {'form': form})

def payment(request):
    return render(request, 'payment.html')

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
    timeframe = request.GET.get('timeframe', 'all')
    registrations = filter_by_timeframe(
        Refugee.objects.all(),
        timeframe,
        date_field='registration_date'
    ).order_by('-registration_date')

    if request.GET.get('download') == 'pdf':
        html = render_to_string('pdf_reports/pdf_registrations.html', {'registrations': registrations})
        pdf = HTML(string=html).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="registrations.pdf"'
        return response

    return render(request, 'view_registrations.html', {
        'registrations': registrations,
        'timeframe': timeframe,  # Pass to template for UI
    })

def view_bookings(request):
    timeframe = request.GET.get('timeframe', 'all')
    bookings = filter_by_timeframe(
        BirthCertificateBooking.objects.select_related('refugee'),
        timeframe,
        date_field='booking_date'
    ).order_by('-booking_date')

    if request.GET.get('download') == 'pdf':
        html = render_to_string('pdf_reports/pdf_bookings.html', {'bookings': bookings})
        pdf = HTML(string=html).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="bookings.pdf"'
        return response

    return render(request, 'view_bookings.html', {
        'bookings': bookings,
        'timeframe': timeframe,  # Pass to template for UI
    })

def view_lost_reports(request):
    timeframe = request.GET.get('timeframe', 'all')
    lost_reports = filter_by_timeframe(
        LostDocumentsReport.objects.select_related('refugee'),
        timeframe,
        date_field='lost_date'
    ).order_by('-lost_date')

    if request.GET.get('download') == 'pdf':
        html = render_to_string('pdf_reports/pdf_lost_reports.html', {'lost_reports': lost_reports})
        pdf = HTML(string=html).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="lost_reports.pdf"'
        return response

    return render(request, 'view_lost_reports.html', {
        'lost_reports': lost_reports,
        'timeframe': timeframe,  # Pass to template for UI
    })
