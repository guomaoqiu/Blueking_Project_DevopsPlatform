# -*- coding: utf-8 -*-
"""BK user model define."""
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)


class BkUserManager(BaseUserManager):
    """BK user manager."""

    def _create_user(self, username, is_staff, is_superuser, **extra_fields):
        """Create and saves a User with the given username and password."""
        if not username:
            raise ValueError(u"'The given username must be set")

        now = timezone.now()
        user = self.model(
            username=username,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=now,

            date_joined=now, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, username, **extra_fields):
        return self._create_user(username, False, False,
                                 **extra_fields)

    def create_superuser(self, username, **extra_fields):
        return self._create_user(username, True, True,
                                 **extra_fields)


class BkUser(AbstractBaseUser, PermissionsMixin):
    """
    BK user.

    username and password are required. Other fields are optional.
    """

    username = models.CharField(u"用户名", max_length=128, unique=True)
    chname = models.CharField(u"中文名", max_length=254, blank=True)
    company = models.CharField(u"公司", max_length=128, blank=True)
    qq = models.CharField(u"QQ号", max_length=32, blank=True)
    phone = models.CharField(u"手机号", max_length=64, blank=True)
    email = models.EmailField(u"邮箱", max_length=254, blank=True)

    is_staff = models.BooleanField(u"普通管理员", default=False, help_text=u"普通管理员可以登录到admin")
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = BkUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """Return the username plus the chinese name, with a space in between."""
        full_name = '%s %s' % (self.username, self.chname)
        return full_name.strip()

    def get_short_name(self):
        """Return the chinese name for the user."""
        return self.chname

    def email_user(self, subject, message, from_email=None):
        """Send an email to this User."""
        send_mail(subject, message, from_email, [self.email])
