from django.contrib.sessions.backends.db import SessionStore

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from main.system.models import User

import logging


logger = logging.getLogger(__name__)

class MyAuthorization(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        s = SessionStore(session_key=token)
        # logger.debug(f"request {request.META}")
        logger.debug(f"session info: {s.items()}")
        user = User.objects.filter(id=s.get("_auth_user_id"))
        if len(user)==0:
            # raise exceptions.AuthenticationFailed('用户未登录')
            logger.debug(f"user is not login !!!")
            raise exceptions.AuthenticationFailed

        user = user[0]
        if user.is_authenticated and token == s.session_key:
            logger.debug(f"{user} is authenticated !!!")
            return (user, token)
        else:
            raise exceptions.AuthenticationFailed('token认证失败')