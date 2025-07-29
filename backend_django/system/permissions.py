from rest_framework import permissions
from rest_framework.request import Request
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

    def check_action_perms(self, view):
        if not hasattr(view, 'perms_map'):
            return []
        perms_map = view.perms_map
        perms = perms_map.get(view.action, [])
        return perms



    def has_permission(self, request, view):
        logger.info(f"Checking permission for {request.user} , action: {view.action}, with perms: {self.check_action_perms(view)}")
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        for role_key in self.allowed_roles:
            if check_user_role(request.user, role_key=role_key):
                # 只要有一个角色满足即可
                return True
        return True

    def has_object_permission(self, request, view, obj):
        logger.info(f"Checking object permission for {request.user} , action: {view.action}, with perms:  {self.check_action_perms(view)}")
        return True



def has_perms(perms=None):
    '''
    给视图函数绑定权限标识
    '''
    def warp_func(view_func):
        if perms and not hasattr(view_func, 'perms'):
            view_func.perms = perms
        return view_func
    return warp_func
