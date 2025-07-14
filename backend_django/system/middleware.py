from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Captcha

import logging
logger = logging.getLogger('user_operation')


class UserOperationMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        if not hasattr(request, 'resolver_match') or not request.resolver_match:
            return response

        if request.method.lower() in ['post', 'get', 'put', 'delete']:
            if not isinstance(request, Request):
                pass
            if request.resolver_match.url_name == 'user-login':
                if response.status_code == status.HTTP_200_OK:
                    logger.info(f'用户登录成功，用户名：{request.user}')
                else:
                    logger.warning(f'用户登录失败，用户名：{request.user}')
            elif request.resolver_match.url_name == 'user-register':
                if response.status_code == status.HTTP_201_CREATED:
                    logger.info(f'新用户注册成功，用户名：{request.user}')
                else:
                    logger.info(f'新用户注册失败，用户名：{request.user}')
            else:
                logger.info(f'用户操作记录，用户名：{request.user}，请求路径：{request.path}，请求方法：{request.method}, 请求视图名称：{request.resolver_match.url_name}')

        return response
    

class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    JWT认证中间件
    """

    def process_response(self, request, response):
        if request.resolver_match.url_name == 'user-logout':
            return response
        if request.user and request.user.is_authenticated:
            auth_token = request.auth
            if not Captcha.objects.filter(uuid=auth_token.get('uuid')).exists():
                response.content = "登录信息已失效，请重新登录！"
                response.status_code = status.HTTP_401_UNAUTHORIZED
            logger.info(f'JWT认证结束：{response}')
        return response