from rest_framework import permissions
from django.db.models import Q

from system.models import *
import logging

logger = logging.getLogger('django')

def check_user_role(user, role_key):
    roles = Role.objects.filter(id__in=user.user_roles.values_list('role_id'))
    if role_key in roles.values_list('role_key', flat=True):
        return True
    else:
        return False

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and check_user_role(request.user, 'admin')

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser or check_user_role(request.user, 'admin'):
            return True
        # 请求用户是否是创建者
        return obj.creator == request.user

class HasRolePermission(permissions.BasePermission):
    def __init__(self, allowed_roles=None):
        self.allowed_roles = allowed_roles or []

    def check_action_perms(self, view, request = None):
        if not hasattr(view, 'get_perms_map'):
            return True
        perms_map = view.get_perms_map()
        perms = perms_map.get(view.action, [])
        # logger.info(f"Checking permissions for action '{view.action}': {perms_map}")
        user = request.user if request else None
        if user and user.is_authenticated:
            if user.is_superuser:
                return True
            else:
                return Menu.objects.filter(
                    role_menus__role__in=user.user_roles.values_list('role_id', flat=True)
                ).filter(
                    Q(perms__in=perms)
                ).exists()
        return False



    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True

        return self.check_action_perms(view, request)

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True

        return self.check_action_perms(view, request)



def has_perms(perms=None):
    '''
    给视图函数绑定权限标识
    '''
    def warp_func(view_func):
        if perms and not hasattr(view_func, 'perms'):
            view_func.perms = perms
        return view_func
    return warp_func
