# urls.py
from django.urls import path
from .views import (DentistListCreateAPIView, DentistRetrieveUpdateDeleteAPIView,
                    WorkDayListAPIView, AppointmentCreateAPIView, AppointmentListForWorkDayAPIView)

urlpatterns = [
    path('dentists/', DentistListCreateAPIView.as_view(),
         name='dentist-list-create'),
    path('dentists/<int:pk>/',
         DentistRetrieveUpdateDeleteAPIView.as_view(), name='dentist-detail'),
    path('workdays/<int:dentist_id>/',
         WorkDayListAPIView.as_view(), name='workday-list'),
    path('appointments/create/', AppointmentCreateAPIView.as_view(),
         name='appointment-create'),
    path('appointments/<int:work_day_id>/',
         AppointmentListForWorkDayAPIView.as_view(), name='appointments-for-day'),
]
