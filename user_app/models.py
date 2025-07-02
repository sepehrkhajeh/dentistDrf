
import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator

INSURANCE_CHOICES = [
    ("بیمه درمانی ایران", "بیمه درمانی ایران"),
    ("بیمه درمان تامین اجتماعی", "بیمه درمان تامین اجتماعی"),
    ("بیمه خدمات درمانی نیروهای مسلح", "بیمه خدمات درمانی نیروهای مسلح"),
    ("بیمه خدمات درمانی (سلامت)", "بیمه خدمات درمانی (سلامت)"),
    ("بیمه دانا", "بیمه دانا"),
    ("بیمه کوثر", "بیمه کوثر"),
    ("بیمه ملت", "بیمه ملت"),
    ("بیمه ما", "بیمه ما"),
    ("بیمه سینا", "بیمه سینا"),
    ("بیمه دی", "بیمه دی"),
    ("بیمه بانک ملی", "بیمه بانک ملی"),
    ("بیمه بانک صادرات", "بیمه بانک صادرات"),
    ("بیمه بانک تجارت", "بیمه بانک تجارت"),
    ("بیمه بانک کشاورزی", "بیمه بانک کشاورزی"),
    ("بیمه بانک سپه", "بیمه بانک سپه"),
    ("بیمه سامان", "بیمه سامان"),
    ("بیمه پاسارگاد", "بیمه پاسارگاد"),
    ("بیمه رازی", "بیمه رازی"),
    ("بیمه کارآفرین", "بیمه کارآفرین"),
    ("بیمه مخابرات ایران", "بیمه مخابرات ایران"),
    ("بیمه پارسیان", "بیمه پارسیان"),
    ("بیمه سایپا", "بیمه سایپا"),
    ("بیمه سرمد", "بیمه سرمد"),
    ("بیمه شهرداری", "بیمه شهرداری"),
    ("بیمه کمک رسان ایران ( SOS )", "بیمه کمک رسان ایران ( SOS )"),
    ("بیمه تجارت نو", "بیمه تجارت نو"),
    ("بیمه آتیه سازان حافظ", "بیمه آتیه سازان حافظ"),
    ("بیمه صدا و سیما", "بیمه صدا و سیما"),
    ("بیمه آسیا", "بیمه آسیا"),
    ("بیمه میهن", "بیمه میهن"),
    ("بیمه آرمان", "بیمه آرمان"),
    ("شرکت ارتقاء سلامت پاسارگاد", "شرکت ارتقاء سلامت پاسارگاد"),
    ("بیمه نوین", "بیمه نوین"),
    ("بیمه بانک رفاه", "بیمه بانک رفاه"),
    ("بیمه البرز", "بیمه البرز"),
    ("بیمه وزارت نیرو (نیرو کارت)", "بیمه وزارت نیرو (نیرو کارت)"),
    ("بیمه معلم", "بیمه معلم"),
    ("بیمه تعاون", "بیمه تعاون"),
    ("کارت طلایی فرهنگیان", "کارت طلایی فرهنگیان"),
    ("صنایع الکترونیک", "صنایع الکترونیک"),
    ("هواپیمایی هما", "هواپیمایی هما"),
    ("هواپیمایی آسمان", "هواپیمایی آسمان"),
    ("بیمه صندوق بازنشستگی کشوری", "بیمه صندوق بازنشستگی کشوری"),
    ("آسپا", "آسپا"),
    ("آتیه سازان ایران", "آتیه سازان ایران"),
    ("سلامت پویا", "سلامت پویا"),
    ("تبسم سپید سلامت", "تبسم سپید سلامت"),
    ("بیمه بانک ملت", "بیمه بانک ملت"),
    ("بیمه آسماری", "بیمه آسماری"),
    ("بیمه مخابرات", "بیمه مخابرات"),
    ("بیمه مهر ایران", "بیمه مهر ایران"),
    ("بیمه بانک مرکزی", "بیمه بانک مرکزی"),
    ("سامانه اقساطی آپ", "سامانه اقساطی آپ"),
    ("بیمه بانک مسکن", "بیمه بانک مسکن"),
    ("کانون وکلا", "کانون وکلا"),
    ("بیمه شرکت نفت فلات قاره", "بیمه شرکت نفت فلات قاره"),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError('شماره تلفن الزامی است')
        user = self.model(phone_number=phone_number, **extra_fields)
        # بدون set_password
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # 📍 لیست شهرهای استان لرستان
    CITY_CHOICES = [
        ('khorramabad', 'خرم‌آباد'),
        ('borujerd', 'بروجرد'),
        ('dorud', 'دورود'),
        ('kuhdasht', 'کوهدشت'),
        ('alishtar', 'الشتر'),
        ('noodshahr', 'نورآباد'),
        ('azna', 'ازنا'),
        ('aligdarzeh', 'الیگودرز'),
        ('sepiddasht', 'سپیددشت'),
        ('poldokhtar', 'پلدختر'),
    ]
    phone_regex = RegexValidator(
        regex=r'^09\d{9}$',
        message="شماره موبایل باید با 09 شروع شود و 11 رقم باشد. مثلاً: 09123456789"
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=11,
        unique=True,  # این خط اضافه بشه
        verbose_name="شماره موبایل"
    )
    first_name = models.CharField(max_length=30, verbose_name="نام")
    last_name = models.CharField(max_length=30, verbose_name="نام خانوادگی")
    insurance = models.CharField(
        max_length=100,
        choices=INSURANCE_CHOICES,
        blank=True,
        null=True,
        verbose_name="نوع بیمه"
    )
    city = models.CharField(
        max_length=20,
        choices=CITY_CHOICES,
        verbose_name="شهر",
        blank=True  
    )
    birth_date = models.CharField(
        max_length=20, verbose_name="تاریخ تولد", blank=True, null=True)
    history_of_illness = models.CharField(
        max_length=255, verbose_name="تاریخچه بیماری", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.phone_number

    def set_password(self, raw_password):
        # غیرفعال کردن ست کردن پسورد
        pass

    def check_password(self, raw_password):
        # همیشه False برگرداندن، چون پسورد نداریم
        return False


class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):

        return self.created_at >= timezone.now() - timedelta(minutes=2)
