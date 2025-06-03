from django.urls import path
from . import views

urlpatterns = [
    path('',views.public_dashboard, name='home'),
    path('register/', views.register_refugee, name='register'),
    path('booking/', views.book_birth_certificate, name='booking'),
    path('report-lost-id/', views.report_lost_id, name='report_lost_id'),
    
]