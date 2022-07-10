from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from .managers import CustomUserManager, UserManager
from .constants import DEFAULT_AVATAR


USER_TYPE = (
    (0, 'Admin'),
    (1, 'User'),
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(_('full name'), max_length=60, blank=True)
    username = models.CharField(_('username'), max_length=40, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.IntegerField(
        blank=True, default=USER_TYPE[1][0], choices=USER_TYPE)
    avatar = models.ImageField(
        upload_to='admin/avatar/', default=DEFAULT_AVATAR, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email_verified = models.BooleanField(
        default=False, verbose_name='email_verified')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name_plural = "All Users"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if(self.user_type == 0):
            self.user_type = 0
            self.is_staff = True
            self.is_superuser = True

        elif(self.user_type == 1):
            self.user_type = 1
            self.is_staff = False
            self.is_superuser = False

        super(CustomUser, self).save(*args, **kwargs)

    def delete_avatar(self):
        img_file = self.avatar
        if not img_file.name == DEFAULT_AVATAR:
            img_file.delete()

    def delete(self):
        img_file = self.avatar
        if not img_file.name == DEFAULT_AVATAR:
            img_file.delete()
        super().delete()


class User(CustomUser):
    bio = models.CharField(max_length=2000, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    github_username = models.CharField(max_length=100, null=True, blank=True)

    objects = UserManager()

    class Meta:
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        self.user_type = 0
        self.is_staff = True
        self.is_superuser = True

        super(User, self).save(*args, **kwargs)
