from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.postgres.fields import ArrayField
from django.db import models

from _spbase.models import BaseActiveTimeStampModel
from spuser.constants import GenderChoices


# User model
class User(AbstractUser):

    id = models.AutoField(primary_key=True, editable=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField( max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices)
    email = models.CharField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=13)
    groups = models.ManyToManyField(Group, related_name="spuser_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="spuser_permissions")


class Profile(BaseActiveTimeStampModel):

    date_of_birth = models.DateField(null=True)
    address = ArrayField(
        models.IntegerField(),
        default=list,
        help_text="Address for the user"
    )
    photo_url = models.URLField(
        default=None, null=True, help_text="An optional image of the user")
    alternate_phone = models.CharField(
        max_length=13,
        null=True,
    )
    preferred_languages = ArrayField(
        models.CharField(max_length=20),
        default=list,
        help_text="Language codes of preferred languages in preference order"
    )
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE, help_text="User", related_name='profile'
    )


# For user token authentication data for validation
class UserAuthToken(BaseActiveTimeStampModel):

    user_id = models.PositiveBigIntegerField()
    token = models.CharField(max_length=500)
    device = models.CharField(max_length=100)
