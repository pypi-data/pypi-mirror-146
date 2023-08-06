from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailBackend(ModelBackend):
    """ A custom authentication backend that allows logging in using email.

    To make use of this backend, add it to your AUTHENTICATION_BACKENDS:
    ```
    AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # the default
    'aims.authentication_backends.EmailBackend']
    ```

    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
        if user.check_password(password):
            return user
        return None
