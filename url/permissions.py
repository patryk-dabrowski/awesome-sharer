from rest_framework.permissions import BasePermission


class IsPermitted(BasePermission):
    def has_object_permission(self, request, view, obj):
        password = request.GET.get('password')

        if not password or not obj.check_password(password):
            return False
        return True
