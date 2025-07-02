from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, OTP


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('phone_number', 'first_name', 'last_name', 'is_staff')
    search_fields = ('phone_number', 'first_name', 'last_name')
    ordering = ('phone_number',)

    # حذف رمز عبور
    fieldsets = (
        (None, {'fields': ('phone_number',)}),
        ('اطلاعات شخصی', {
         'fields': ('first_name', 'last_name', 'insurance', 'city')}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'first_name', 'last_name', 'is_staff', 'is_superuser'),
        }),
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('code', 'phone_number')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
