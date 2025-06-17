from django.urls import path
from .views import (
    manage_dashboard,
    manage_refugees,
    add_refugee,
    edit_refugee,
    delete_refugee,
    manage_bookings,
    add_booking,
    edit_booking,
    delete_booking,
    manage_lost_documents,
    add_lost_document_report,
    edit_lost_document_report,
    delete_lost_document_report,
)

urlpatterns = [
    path('staff/', manage_dashboard, name='manage_dashboard'),

    # Refugee URLs
    path('refugees/', manage_refugees, name='manage_refugees'),
    path('refugees/add/', add_refugee, name='add_refugee'),
    path('refugees/edit/<int:pk>/', edit_refugee, name='edit_refugee'),
    path('refugees/delete/<int:pk>/', delete_refugee, name='delete_refugee'),

    # Booking URLs
    path('bookings/', manage_bookings, name='manage_bookings'),
    path('bookings/add/', add_booking, name='add_booking'),
    path('bookings/edit/<int:pk>/', edit_booking, name='edit_booking'),
    path('bookings/delete/<int:pk>/', delete_booking, name='delete_booking'),

    # Lost Document Reports URLs
    path('lost-documents/', manage_lost_documents, name='manage_lost_documents'),
    path('lost-documents/add/', add_lost_document_report, name='add_lost_document_report'),
    path('lost-documents/edit/<int:pk>/', edit_lost_document_report, name='edit_lost_document_report'),
    path('lost-documents/delete/<int:pk>/', delete_lost_document_report, name='delete_lost_document_report'),
]
