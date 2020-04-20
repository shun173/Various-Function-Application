from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone

from ecapp.models import Product


class UserManager(BaseUserManager):
    """カスタムユーザーマネージャー"""
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル"""
    initial_point = 50000
    email = models.EmailField("メールアドレス", unique=True)
    username = models.CharField("username", max_length=50)
    address = models.CharField(max_length=100, blank=True)
    point = models.PositiveIntegerField(default=initial_point)
    fav_products = models.ManyToManyField(Product, blank=True)
    is_staff = models.BooleanField("is_staff", default=False)
    is_active = models.BooleanField("is_activ", default=True)
    date_joined = models.DateTimeField("date_joind", default=timezone.now)
    last_login = models.DateTimeField("last_login", blank=True, null=True)

    objecs = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user. """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.email


@receiver(user_logged_in)
def user_loged_in_callback(sender, request, user, **kwargs):
    """ログインした際に呼ばれる"""
    user.last_login = timezone.now()
    user.save()
