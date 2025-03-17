from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
import hashlib
# from main.system.models import User

UserModel = get_user_model()

import logging

logger = logging.getLogger(__name__)

class UserBackend(BaseBackend):
  def authenticate(self, request, username = None, password = None, **kwargs):
    if username and password:
      try:
        user = UserModel._default_manager.get(login_name=username)
        h = hashlib.md5()
        h.update(password.encode())
        logger.debug(f"crypto password: {h.hexdigest()},  raw password: {user.password}")
        if h.hexdigest() == user.password:
          return user
        # # if user.check_password(password):
        # #   return user

      except UserModel.DoesNotExist:
        logger.info(f"User does not exist")
        return None
    return None