import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger('user_operation')

class UserOperationMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        if not hasattr(request, 'resolver_match') or not request.resolver_match:
            return response
        logger.info(f'process_response => {request.resolver_match}')

        if request.resolver_match.url_name == 'user-login':
            action = request.method.lower()
            if action in ['post']:
                logger.info(f'用户{request.POST.get("username")}登录成功')
        if request.resolver_match.url_name == 'user-register':
            action = request.method.lower()
            if action in ['post']:
                logger.info(f'新用户注册，用户名：{request.POST.get("username")}')

        return response