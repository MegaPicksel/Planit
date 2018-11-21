from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser)


class UserManager(BaseUserManager):
    """ Model manager, as per django documentation."""

    def create_user(self, email, password=None):
        """ Create a normal user, validation done with email and password."""
        if not email:
            raise ValueError('Username must be a valild email address.')

        user = self.model(
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """ Create a superuser, this method calls the create_user method,and adds to it."""
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    """ This class defines the user. """

    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(verbose_name='first name', max_length=255)
    last_name = models.CharField(verbose_name='last name', max_length=255)
    city = models.CharField(verbose_name='city', max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, planner):
        return True

    @property
    def is_staff(self):
        return self.is_admin
