from django.contrib import admin
from .models import BirthCertificateBooking, Refugee,LostIDReport

# Register your models here.
admin.site.register(BirthCertificateBooking)
admin.site.register(Refugee)
admin.site.register(LostIDReport)
