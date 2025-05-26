from rest_framework import permissions
from system.models import User,Role


def check_user_role(user, role_key):
    role = Role.objects.filter(id__in=user.user_roles.values_list('role_id', flat=True))
    if role.exists():
        return role.first().role_key == role_key
    return False

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and check_user_role(request.user, 'admin')

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        # 请求用户是否是管理员角色
        if request.user.is_superuser or check_user_role(request.user, 'admin'):
            return True
        # 请求用户是否是创建者
        return obj.creator == request.user

class HasRolePermission(permissions.BasePermission):
    def __init__(self, allowed_roles=None):
        self.allowed_roles = allowed_roles or []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        for role_key in self.allowed_roles:
            if check_user_role(request.user, role_key=role_key):
                # 只要有一个角色满足即可
                return True
        return False