from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        # فرض می‌کنیم مدل CustomUser است و می‌خواهیم فقط اجازه بدهیم صاحب رکورد عملیات انجام دهد
        return obj == request.user
