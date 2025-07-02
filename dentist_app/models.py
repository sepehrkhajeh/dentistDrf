from django.db import models
from django.utils import timezone
from user_app.models import CustomUser
import django_jalali.db.models as jmodels


class DentistModel(models.Model):
    CITY_CHOICES = [
        ('tehran', 'تهران'),
        ('mashhad', 'مشهد'),
        ('isfahan', 'اصفهان'),
        ('shiraz', 'شیراز'),
        ('tabriz', 'تبریز'),
        ('ahvaz', 'اهواز'),
        ('karaj', 'کرج'),
        ('qom', 'قم'),
        ('kermanshah', 'کرمانشاه'),
        ('rasht', 'رشت'),
        ('urmia', 'ارومیه'),
        ('zahedan', 'زاهدان'),
        ('sanandaj', 'سنندج'),
        ('gorgan', 'گرگان'),
        ('ardabil', 'اردبیل'),
    ]

    full_name = models.CharField(max_length=100, verbose_name="نام کامل")
    field_of_work = models.CharField(
        max_length=100, verbose_name="زمینه فعالیت")
    medical_system_code = models.CharField(
        max_length=20, unique=True, verbose_name="کد نظام پزشکی")
    phone_number = models.CharField(max_length=15, verbose_name="شماره موبایل")
    city = models.CharField(
        max_length=20, choices=CITY_CHOICES, verbose_name="شهر")
    description = models.TextField(
        blank=True, null=True, verbose_name="توضیحات")
    created_at = jmodels.jDateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"{self.full_name} - {self.city}"


class WorkDay(models.Model):
    dentist = models.ForeignKey(
        DentistModel, on_delete=models.CASCADE, related_name='workdays')
    date = jmodels.jDateField(verbose_name="تاریخ")
    created_at = jmodels.jDateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        unique_together = ['dentist', 'date']

    def __str__(self):
        return f"{self.dentist.full_name} - {self.date}"


class Appointment(models.Model):
    work_day = models.ForeignKey(
        WorkDay, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='appointments')
    time = models.TimeField(verbose_name="ساعت نوبت")
    description = models.TextField(
        blank=True, null=True, verbose_name="توضیحات بیمار")
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده؟")

    class Meta:
        unique_together = ['work_day', 'time']

    def __str__(self):
        return f"{self.patient.first_name} - {self.work_day.date} - {self.time}"
