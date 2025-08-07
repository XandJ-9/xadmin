from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from main.utils.util_request import convert_to_restf_request
from .models import Captcha

import logging,json
logger = logging.getLogger('user_operation')


class UserOperationMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        if not hasattr(request, 'resolver_match') or not request.resolver_match:
            return response
        
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.data)
        else:
            # 将httprequest转换为rest_framework.request.Request对象
            new_request = convert_to_restf_request(request)
            data = new_request.data

        if request.user and request.user.is_authenticated:
                logger.info(f'用户操作记录，用户名：{request.user}，请求路径：{request.path}，请求方法：{request.method}, 请求视图名称：{request.resolver_match.url_name}')
        else:
            # 只有表单请求可以获取用户名称
            if request.method == 'POST' and request.resolver_match.url_name == 'user-login':
                # username = request.data.get('username')
                username = request.POST.get('username')
                if response.status_code == status.HTTP_200_OK:
                    logger.info(f'用户登录成功，用户名：{username}')
                else:
                    logger.warning(f'用户登录失败，用户名：{username}')
            elif request.method == 'POST' and request.resolver_match.url_name == 'user-register':
                username = request.POST.get('username')
                if response.status_code == status.HTTP_201_CREATED:
                    logger.info(f'新用户注册成功，用户名：{username}')
                else:
                    logger.info(f'新用户注册失败，用户名：{username}')
        return response
    

class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    JWT认证中间件
    """

    def process_response(self, request, response):
        if not hasattr(request, 'resolver_match') or not request.resolver_match:
            return response
        
        if request.resolver_match.url_name == 'user-logout':
            return response
        if request.user and request.user.is_authenticated:
            auth_token = request.auth
            if not Captcha.objects.filter(uuid=auth_token.get('uuid')).exists():
                response.content = "登录信息已失效，请重新登录！"
                response.status_code = status.HTTP_401_UNAUTHORIZED
        return response