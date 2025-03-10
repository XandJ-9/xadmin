import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger('user_operation')

class UserOperationMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(view_func, 'view_class') and view_func.view_class.__name__ == 'UserViewSet':
            action = getattr(view_func.view_class, request.method.lower(), None)
            if action and action.__name__ in ['login', 'register']:
                username = request.data.get('username', '')
                logger.info(f'用户 {username} 尝试{"登录" if action.__name__ == "login" else "注册"}')
        return None

    def process_response(self, request, response):
        if hasattr(request, '_view_func') and hasattr(request._view_func, 'view_class'):
            if request._view_func.view_class.__name__ == 'UserViewSet':
                action = getattr(request._view_func.view_class, request.method.lower(), None)
                if action and action.__name__ in ['login', 'register']:
                    username = request.data.get('username', '')
                    status_code = response.status_code
                    if status_code == 200 or status_code == 201:
                        logger.info(f'用户 {username} {"登录" if action.__name__ == "login" else "注册"}成功')
                    else:
                        logger.warning(f'用户 {username} {"登录" if action.__name__ == "login" else "注册"}失败')
        return response

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 记录用户操作
        if hasattr(request, 'user') and request.user.is_authenticated:
            logger.info(f'User {request.user.username} (role: {request.user.role}) accessing {request.path} with method {request.method}')

            # 获取用户角色
            user_role = request.user.role

            # 基于角色的访问控制
            if not self._check_role_permission(request.path, request.method, user_role):
                logger.warning(f'Access denied for user {request.user.username} (role: {user_role}) to {request.path}')
                return JsonResponse({
                    'error': '您没有权限执行此操作'
                }, status=403)

        response = self.get_response(request)
        return response

    def _check_role_permission(self, path, method, role):
        # 超级管理员可以访问所有资源
        if role == 'superuser':
            return True

        # 管理员可以访问除了系统配置外的所有资源
        if role == 'admin':
            if not path.startswith('/api/system/'):
                return True

        # 普通用户只能访问基本资源和自己的数据
        if role == 'user':
            allowed_paths = [
                '/api/users/profile/',
                '/api/users/password/',
                '/api/common/',
                '/api/users/login/',
                '/api/users/register/'
            ]
            if method in ['GET', 'PUT', 'PATCH'] and path.startswith('/api/users/'):
                return True  # 允许用户访问自己的数据
            return any(path.startswith(allowed_path) for allowed_path in allowed_paths)

        return False