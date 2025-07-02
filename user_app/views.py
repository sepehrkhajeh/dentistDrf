from .permissions import IsOwner  # مسیر را بر اساس پروژه تنظیم کن
import random
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from .models import CustomUser, OTP
from .serializers import RegisterSerializer, LoginRequestSerializer, OTPVerifySerializer, CustomUserSerializer

# ثبت‌نام


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']

        if CustomUser.objects.filter(phone_number=phone).exists():
            return Response({'detail': 'این شماره قبلاً ثبت شده است.'}, status=400)

        # ساخت کاربر بدون پسورد
        user = CustomUser.objects.create(
            phone_number=phone,
            first_name=first_name,
            last_name=last_name
        )

        # ساخت کد تایید
        code = str(random.randint(100000, 999999))
        print(code)
        OTP.objects.create(phone_number=phone, code=code)

        return Response({'detail': f'کد تایید برای {phone} ارسال شد (کد: {code})'}, status=200)

# لاگین - ارسال کد تایید


class LoginRequestView(APIView):
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']

        try:
            user = CustomUser.objects.get(phone_number=phone)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'این شماره ثبت نشده است.'}, status=404)

        # ارسال کد تایید
        code = str(random.randint(100000, 999999))
        OTP.objects.create(phone_number=phone, code=code)
        print(code)
        return Response({'detail': f'کد تایید ارسال شد (کد: {code})'}, status=200)

# تأیید کد و دریافت JWT


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        try:
            otp = OTP.objects.filter(
                phone_number=phone, code=code).latest('created_at')
        except OTP.DoesNotExist:
            return Response({'detail': 'کد تایید اشتباه است.'}, status=400)

        if not otp.is_valid():
            return Response({'detail': 'کد تایید منقضی شده است.'}, status=400)

        try:
            user = CustomUser.objects.get(phone_number=phone)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'کاربر یافت نشد.'}, status=404)

        # پاک کردن همه کدها بعد از ورود موفق
        OTP.objects.filter(phone_number=phone).delete()

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })


class CustomUserListCreateAPIView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)


class CustomUserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        self.check_object_permissions(
            self.request, user)  # چک کردن پرمیژن روی آبجکت
        return user

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
