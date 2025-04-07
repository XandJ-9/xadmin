from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
from .models import User
import logging

logger = logging.getLogger('django')

def get_user_from_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return AnonymousUser()

    try:
        token = auth_header.split(' ')[1]
        access_token = AccessToken(token)
        user_id = access_token.get('user_id')
        user = User.objects.get(id=user_id)
        return user
    except (InvalidToken, TokenError, User.DoesNotExist) as e:
        # logger.error(f'Token authentication failed: {str(e)}')
        return AnonymousUser()

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: get_user_from_token(request))
        if request.user.is_authenticated:
            logger.info(f'User {request.user.username} (role: {request.user.role}) accessed {request.path} with method {request.method}')
        return self.get_response(request)