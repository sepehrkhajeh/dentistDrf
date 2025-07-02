from django.contrib import admin

from .models import WorkDay, Appointment
from django_jalali.admin.filters import JDateFieldListFilter


@admin.register(WorkDay)
class WorkDayAdmin(admin.ModelAdmin):
    list_display = ['id', 'dentist', 'date']
    list_filter = ['date', 'dentist']
    search_fields = ['dentist__first_name', 'dentist__last_name']
    ordering = ['-date']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'work_day', 'time', 'is_approved']
    list_filter = ['is_approved', 'work_day__date']
    search_fields = ['patient__phone_number', 'description']
    ordering = ['work_day__date', 'time']
