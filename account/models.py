from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

import os


def upload_profile_location(instance, filename):
    return 'profile_pictures/{user}/{filename}'.format(
        user=instance.username, filename=filename
    )

def upload_banner_location(instance, filename):
    return 'banner_pictures/{user}/{filename}'.format(
        user=instance.username, filename=filename
    )

class MyAccountManager(BaseUserManager):
    # Here in parameters you have to include everything from REQUIRED_FIELDS    
    def create_user(self, email, username, full_name, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an username")
        if not full_name:
            raise ValueError("User must have a full name")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            full_name=full_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            full_name=full_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class Account(AbstractBaseUser):
    # These fields are required by the mother model
    email        = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username     = models.CharField(max_length=30, unique=True)
    date_joined  = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login   = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # These fields are added by me
    full_name     = models.CharField(max_length=60)
    date_of_birth = models.DateField(verbose_name="birth date", editable=True, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=upload_profile_location, blank=True, default='default_images/default_profile.png')
    banner_picture = models.ImageField(upload_to=upload_banner_location, blank=True, default='default_images/default_banner.png')
    residency = models.CharField(max_length=85, blank=True)
    about = models.TextField(blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followers_users", symmetrical=False, blank=True) 
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followed_users", symmetrical=False, blank=True)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('E', 'Something else')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "full_name"]

    objects = MyAccountManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(pre_save, sender=Account)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from AWS S3
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_profile = sender.objects.get(pk=instance.pk).profile_picture
        old_banner = sender.objects.get(pk=instance.pk).banner_picture
    except sender.DoesNotExist:
        return False

    new_profile = instance.profile_picture
    new_banner = instance.banner_picture

    if not old_profile == new_profile:
        # if os.path.isfile(old_profile.path):
        #     os.remove(old_profile.path)
        print(old_profile)
        print(old_profile.url)
        if not 'default_images/default_profile.png' == old_profile:
            old_profile.delete(save=False)

    if not old_banner == new_banner:
        # if os.path.isfile(old_banner.path):
        #     os.remove(old_banner.path)
        print(old_banner)
        print(old_banner.url)
        if not 'default_images/default_banner.png' == old_banner:
            old_banner.delete(save=False)