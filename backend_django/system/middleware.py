import logging
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status

logger = logging.getLogger('user_operation')

class UserOperationMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        if not hasattr(request, 'resolver_match') or not request.resolver_match:
            return response

        if request.method.lower() in ['post', 'get', 'put', 'delete']:
          if request.resolver_match.url_name == 'user-login':
              token = response.data.get('token')
              if token:
                  logger.info(f'用户登录成功，用户名：{request.POST.get("username")}')
          if request.resolver_match.url_name == 'user-register':
              if response.status_code == status.HTTP_201_CREATED:
                  logger.info(f'新用户注册成功，用户名：{request.POST.get("username")}')
              else:
                  logger.info(f'新用户注册失败，用户名：{request.POST.get("username")}')

        return response