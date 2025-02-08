from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        abstract = True


class BaseActiveModel(BaseModel):
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class BaseTimeStampModel(BaseModel):
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class BaseActiveTimeStampModel(BaseTimeStampModel):
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class BaseExtraColumnModel(models.Model):
    extra_columns = models.JSONField(default=dict)

    class Meta:
        abstract = True