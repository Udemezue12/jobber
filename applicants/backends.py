from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
import bcrypt
import logging

logger = logging.getLogger(__name__)

class BcryptBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        CustomUser = get_user_model()
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            logger.debug(f"User '{username}' does not exist.")
            return None

        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        else:
            logger.debug(f"Password for user '{username}' is incorrect.")
            return None

    def get_user(self, user_id):
        CustomUser = get_user_model()
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
