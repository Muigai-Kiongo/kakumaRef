from django.urls import path
from .views import manage_dashboard, manage_refugees, manage_bookings, manage_reports

urlpatterns = [
    path('staff/', manage_dashboard, name='manage_dashboard'),
    path('refugees/', manage_refugees, name='manage_refugees'),
    path('bookings/', manage_bookings, name='manage_bookings'),
    path('reports/', manage_reports, name='manage_reports'),
]
