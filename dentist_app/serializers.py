# serializers.py
from .models import WorkDay, Appointment
from rest_framework import serializers
from .models import DentistModel


class DentistSerializer(serializers.ModelSerializer):
    class Meta:
        model = DentistModel
        fields = '__all__'


class WorkDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDay
        fields = ['id', 'dentist', 'date']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'work_day', 'patient',
                  'time', 'description', 'is_approved']
        # این‌ها به‌صورت خودکار ست می‌شوند
        read_only_fields = ['patient', 'is_approved']
