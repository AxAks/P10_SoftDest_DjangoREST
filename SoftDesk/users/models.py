from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Extends the Basic User class without adding anything to it
    in order to be able to override it easily in the future, if needed
    """
    pass
