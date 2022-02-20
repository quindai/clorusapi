from rest_framework import permissions
from accounts.models.apiuser import APIUser

class BasicPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = APIUser.objects.get(user=request.user.pk)

        if user.user_type == '2':
            if request.method in ['PUT','POST']:
                return False
            if request.method in permissions.SAFE_METHODS:
                try:
                    if view.kwargs['pk'] != user.active_company.pk:
                        return False
                except KeyError:
                    return False
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        return True