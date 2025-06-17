from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from booking.models import Refugee, BirthCertificateBooking, LostDocumentsReport
from booking.forms import (
    RefugeeForm,
    BirthCertificateBookingForm,
    LostDocumentsReportForm,
    LostIDDetailsForm,
    ManifestDetailsForm,
)

def staff_required(view_func):
    """Custom decorator to check if the user is a staff member."""
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view

@login_required
@staff_required
def manage_dashboard(request):
    total_refugees = Refugee.objects.count()
    total_bookings = BirthCertificateBooking.objects.count()
    total_lost_reports = LostDocumentsReport.objects.count()

    context = {
        'total_refugees': total_refugees,
        'total_bookings': total_bookings,
        'total_lost_reports': total_lost_reports,
    }
    return render(request, 'manage_dashboard.html', context)

@login_required
@staff_required
def manage_refugees(request):
    search_query = request.GET.get('search', '')
    refugees = Refugee.objects.filter(
        Q(full_name__icontains=search_query) | Q(nationality__icontains=search_query)
    ).order_by('full_name')

    paginator = Paginator(refugees, 10)  # 10 per page
    page_number = request.GET.get('page')
    refugees_page = paginator.get_page(page_number)

    return render(request, 'manage_refugees.html', {
        'refugees': refugees_page,
        'search_query': search_query,
    })

@login_required
@staff_required
def add_refugee(request):
    if request.method == 'POST':
        form = RefugeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_refugees')
    else:
        form = RefugeeForm()
    return render(request, 'edit_refugee.html', {'form': form, 'action': 'Add'})

@login_required
@staff_required
def edit_refugee(request, pk):
    refugee = get_object_or_404(Refugee, pk=pk)
    if request.method == 'POST':
        form = RefugeeForm(request.POST, instance=refugee)
        if form.is_valid():
            form.save()
            return redirect('manage_refugees')
    else:
        form = RefugeeForm(instance=refugee)
    return render(request, 'edit_refugee.html', {'form': form, 'action': 'Edit', 'refugee': refugee})

@login_required
@staff_required
def delete_refugee(request, pk):
    refugee = get_object_or_404(Refugee, pk=pk)
    if request.method == 'POST':
        refugee.delete()
        return redirect('manage_refugees')
    return render(request, 'confirm_delete.html', {'object': refugee, 'type': 'Refugee'})

@login_required
@staff_required
def manage_bookings(request):
    search_query = request.GET.get('search', '')
    bookings = BirthCertificateBooking.objects.filter(
        Q(refugee__full_name__icontains=search_query) | Q(status__icontains=search_query)
    ).order_by('-booking_date')

    paginator = Paginator(bookings, 10)
    page_number = request.GET.get('page')
    bookings_page = paginator.get_page(page_number)

    return render(request, 'manage_bookings.html', {
        'bookings': bookings_page,
        'search_query': search_query,
    })

@login_required
@staff_required
def add_booking(request):
    if request.method == 'POST':
        form = BirthCertificateBookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_bookings')
    else:
        form = BirthCertificateBookingForm()
    return render(request, 'edit_booking.html', {'form': form, 'action': 'Add'})

@login_required
@staff_required
def edit_booking(request, pk):
    booking = get_object_or_404(BirthCertificateBooking, pk=pk)
    if request.method == 'POST':
        form = BirthCertificateBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('manage_bookings')
    else:
        form = BirthCertificateBookingForm(instance=booking)
    return render(request, 'edit_booking.html', {'form': form, 'action': 'Edit', 'booking': booking})

@login_required
@staff_required
def delete_booking(request, pk):
    booking = get_object_or_404(BirthCertificateBooking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('manage_bookings')
    return render(request, 'confirm_delete.html', {'object': booking, 'type': 'Booking'})

@login_required
@staff_required
def manage_lost_documents(request):
    search_query = request.GET.get('search', '')
    reports = LostDocumentsReport.objects.filter(
        Q(refugee__full_name__icontains=search_query) |
        Q(document_type__icontains=search_query) |
        Q(status__icontains=search_query)
    ).order_by('-lost_date')

    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    reports_page = paginator.get_page(page_number)

    return render(request, 'manage_lost_documents.html', {
        'reports': reports_page,
        'search_query': search_query,
    })

@login_required
@staff_required
def add_lost_document_report(request):
    if request.method == 'POST':
        report_form = LostDocumentsReportForm(request.POST)
        id_form = LostIDDetailsForm(request.POST)
        manifest_form = ManifestDetailsForm(request.POST)
        if report_form.is_valid():
            lost_document_report = report_form.save()
            if lost_document_report.document_type == 'ID' and id_form.is_valid():
                id_details = id_form.save(commit=False)
                id_details.lost_document_report = lost_document_report
                id_details.save()
            elif lost_document_report.document_type == 'MANIFEST' and manifest_form.is_valid():
                manifest_details = manifest_form.save(commit=False)
                manifest_details.lost_document_report = lost_document_report
                manifest_details.save()
            return redirect('manage_lost_documents')
    else:
        report_form = LostDocumentsReportForm()
        id_form = LostIDDetailsForm()
        manifest_form = ManifestDetailsForm()
    return render(request, 'edit_lost_document.html', {
        'report_form': report_form,
        'id_form': id_form,
        'manifest_form': manifest_form,
        'action': 'Add'
    })

@login_required
@staff_required
def edit_lost_document_report(request, pk):
    lost_document_report = get_object_or_404(LostDocumentsReport, pk=pk)
    try:
        id_details = lost_document_report.id_details
    except LostIDDetails.DoesNotExist:
        id_details = None
    try:
        manifest_details = lost_document_report.manifest_details
    except ManifestDetails.DoesNotExist:
        manifest_details = None

    if request.method == 'POST':
        report_form = LostDocumentsReportForm(request.POST, instance=lost_document_report)
        id_form = LostIDDetailsForm(request.POST, instance=id_details)
        manifest_form = ManifestDetailsForm(request.POST, instance=manifest_details)
        if report_form.is_valid():
            lost_document_report = report_form.save()
            if lost_document_report.document_type == 'ID' and id_form.is_valid():
                id_details = id_form.save(commit=False)
                id_details.lost_document_report = lost_document_report
                id_details.save()
            elif lost_document_report.document_type == 'MANIFEST' and manifest_form.is_valid():
                manifest_details = manifest_form.save(commit=False)
                manifest_details.lost_document_report = lost_document_report
                manifest_details.save()
            return redirect('manage_lost_documents')
    else:
        report_form = LostDocumentsReportForm(instance=lost_document_report)
        id_form = LostIDDetailsForm(instance=id_details)
        manifest_form = ManifestDetailsForm(instance=manifest_details)

    return render(request, 'edit_lost_document.html', {
        'report_form': report_form,
        'id_form': id_form,
        'manifest_form': manifest_form,
        'action': 'Edit',
        'lost_document_report': lost_document_report,
    })

@login_required
@staff_required
def delete_lost_document_report(request, pk):
    lost_document_report = get_object_or_404(LostDocumentsReport, pk=pk)
    if request.method == 'POST':
        lost_document_report.delete()
        return redirect('manage_lost_documents')
    return render(request, 'confirm_delete.html', {'object': lost_document_report, 'type': 'Lost Document Report'})
