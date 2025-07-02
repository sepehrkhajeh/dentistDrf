from django.urls import path
from .views import RegisterView, LoginRequestView, VerifyOTPView, CustomUserListCreateAPIView, CustomUserDetailAPIView

urlpatterns = [
    path('', CustomUserListCreateAPIView.as_view(), name='user-list-create'),
    path('<int:pk>/', CustomUserDetailAPIView.as_view(), name='user-detail'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginRequestView.as_view(), name='login'),
    path('auth/verify/', VerifyOTPView.as_view(), name='verify_otp'),
]
