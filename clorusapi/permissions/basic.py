from rest_framework import permissions
from accounts.models.apiuser import APIUser
class BasicPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = APIUser.objects.get(user=request.user.pk)

        if request.method == 'GET' and user.user_type == '2':
            return True
        if request.method in ['GET', 'PUT'] and user.user_type == '1':
            return True
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        return True