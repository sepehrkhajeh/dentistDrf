# 🦷 Dentist DRF Project

این پروژه یک سیستم نوبت‌دهی دندان‌پزشکی با استفاده از Django و Django REST Framework است. در این سیستم کاربران می‌توانند ثبت‌نام کنند، پزشکان و روزهای کاری را مشاهده و نوبت رزرو کنند.

---

## ⚙️ تکنولوژی‌ها

- Python 3.8+
- Django
- Django REST Framework (DRF)
- SQLite (قابل تغییر)
- Persian Date (django-jalali)
- JWT Auth (در صورت نیاز)

---

## 📦 پیش‌نیازها

قبل از راه‌اندازی پروژه، مطمئن شوید موارد زیر نصب هستند:

- Python 3.8+
- Git
- pip
- virtualenv

---

## 🚀 راه‌اندازی پروژه

### 1. دریافت پروژه از GitHub

```bash
git clone https://github.com/sepehrkhajeh/dentistDrf.git
cd dentistDrf

ایجاد محیط مجازی
# برای Windows:
python -m venv venv
venv\Scripts\activate

# برای Mac/Linux:
python3 -m venv venv
source venv/bin/activate
نصب نیازمندی ها
### install requirements 
pip install -r requirements.txt

تنظیمات پایگاه داده و مایگریشن‌ها
python manage.py makemigrations
python manage.py migrate
ساخت کاربر ادمین
python manage.py createsuperuser
اجرای پروژه
python manage.py runserver



