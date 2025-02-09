from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from _spbase.models import BaseActiveTimeStampModel
from spuser.constants import GenderChoices


class User(AbstractUser):

    id = models.AutoField(primary_key=True, editable=False)
    username_validator = UnicodeUsernameValidator()
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    email = models.EmailField(db_index=True)
    username = models.CharField(
        _("username"),
        max_length=300,
        unique=True,
        help_text=_(
            "Required. 300 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    gender = models.CharField(max_length=10, choices=GenderChoices)
    phone = models.CharField(max_length=13)
    groups = models.ManyToManyField(Group, related_name="spuser_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="spuser_permissions")
    token = models.CharField(max_length=500, blank=True, null=True)



class Profile(BaseActiveTimeStampModel):

    interested_fields = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text="Interested fields in preference order"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    preferred_languages = ArrayField(
        models.CharField(max_length=20),
        default=list,
        help_text="Language codes of preferred languages in preference order"
    )
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE, help_text="User", related_name='profile'
    )

