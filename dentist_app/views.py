# views.py
from .serializers import AppointmentSerializer, WorkDaySerializer
from .models import Appointment, WorkDay
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination

from .models import DentistModel
from .serializers import DentistSerializer


class DentistListCreateAPIView(APIView):
    def get(self, request):
        dentists = DentistModel.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10  # یا استفاده از DentistPagination()
        result_page = paginator.paginate_queryset(dentists, request)
        serializer = DentistSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = DentistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DentistRetrieveUpdateDeleteAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(DentistModel, pk=pk)

    def get(self, request, pk):
        dentist = self.get_object(pk)
        serializer = DentistSerializer(dentist)
        return Response(serializer.data)

    def put(self, request, pk):
        dentist = self.get_object(pk)
        serializer = DentistSerializer(dentist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        dentist = self.get_object(pk)
        dentist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AppointmentCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['patient'] = request.user.id
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkDayListAPIView(APIView):
    """لیست روزهای کاری یک دندان‌پزشک خاص"""

    def get(self, request, dentist_id):
        work_days = WorkDay.objects.filter(dentist_id=dentist_id)
        serializer = WorkDaySerializer(work_days, many=True)
        return Response(serializer.data)


class AppointmentCreateAPIView(APIView):
    """ثبت نوبت توسط کاربر لاگین‌شده"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentListForWorkDayAPIView(APIView):
    """لیست نوبت‌های یک روز خاص"""

    def get(self, request, work_day_id):
        appointments = Appointment.objects.filter(work_day_id=work_day_id)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
