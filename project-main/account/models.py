from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class Branch(models.Model):
    class Meta:
        verbose_name_plural = _('branches')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('user')
        
    email = models.EmailField(_('email address'), unique=True)
    branch = models.ForeignKey(Branch, related_name='branch', blank=True, null=True, on_delete=models.SET_NULL)

    first_name = models.CharField(_('first name'), max_length=255)
    last_name = models.CharField(_('last name'), max_length=255)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

