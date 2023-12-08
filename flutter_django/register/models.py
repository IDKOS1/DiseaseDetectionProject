from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Email을 입력해주세요.')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    #def create_user(self, username, email, password=None, **extra_fields):
    #    extra_fields.setdefault('is_staff', False)
    #    extra_fields.setdefault('is_superuser', False)
    #    return self._create_user(username, email, password, **extra_fields)

    #def create_superuser(self, username, email, password, **extra_fields):
    #    extra_fields.setdefault('is_staff', True)
    #    extra_fields.setdefault('is_superuser', True)
    #    if extra_fields.get('is_staff') is not True:
    #        raise ValueError('is_staff=True일 필요가 있습니다.')
    #    if extra_fields.get('is_superuser') is not True:
    #        raise ValueError('is_superuser=True일 필요가 있습니다.')
    #    return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('M', _("Male")),
        ('F', _("Female")),
    ]
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=50, validators=[username_validator], blank=True)
    birth = models.DateField(_("Birth Date"), blank=True, null=True)
    gender = models.CharField(_("Gender"), max_length=1, choices=GENDER_CHOICES, null=True)
    number = models.CharField(_("Phone Number"), max_length=15, blank=True)
    farm = models.CharField(_("Farm Name"), max_length=30, blank=True)
    #is_staff = models.BooleanField(_("staff status"), default=False)
    #is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class ImageUpload(models.Model):
    location = models.CharField(max_length=1000, default='x', primary_key=True, unique=True)
    upload_user = models.ForeignKey(User, related_name="uploaded", on_delete=models.SET_NULL,
                                    null=True, db_column="user_id")
    upload_date = models.DateTimeField("date joined", default=timezone.now)
    number_images = models.IntegerField(default=0)
    is_done = models.BooleanField("Inspection complete", default=False)
    Edwardsiella = models.DecimalField(max_digits=4, decimal_places=4, default=Decimal('0.0000'))
    Vibrio = models.DecimalField(max_digits=4, decimal_places=4, default=Decimal('0.0000'))
    Streptococcus = models.DecimalField(max_digits=4, decimal_places=4, default=Decimal('0.0000'))
    Tenacibaculumn = models.DecimalField(max_digits=4, decimal_places=4, default=Decimal('0.0000'))
    Enteromyxum = models.DecimalField(max_digits=4, decimal_places=4, default=Decimal('0.0000'))
    Miamiensis = models.DecimalField(max_digits=4, decimal_places=4, default=Decimal('0.0000'))
    VHSV = models.DecimalField(max_digits=4, decimal_places=4, default=Decimal('0.0000'))

