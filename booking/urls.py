from django.urls import path
from . import views

urlpatterns = [
    path('', views.public_dashboard, name='home'),
    path('register/', views.register_refugee, name='register-refugee'),
    path('booking/', views.book_birth_certificate, name='booking'),
    path('payment/',views.payment,name='payment'),
    path('report-lost-docs/', views.report_lost_documents, name='report_lost_docs'),

    path('registrations/', views.view_registrations, name='view_registrations'),
    path('bookings/', views.view_bookings, name='view_bookings'),
    path('lost-reports/', views.view_lost_reports, name='view_lost_reports'),
]
