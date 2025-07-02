from user_app.models import CustomUser
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class LoginRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField(max_length=6)
# serializers.py


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'phone_number',
            'first_name',
            'last_name',
            'birth_date',
            'history_of_illness',
            'insurance',
            'city',
            'is_active',
            'is_staff',
        ]
