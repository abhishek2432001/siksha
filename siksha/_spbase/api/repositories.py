from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models


class BaseRepository:
    model_class = None

    def __init__(self):
        self.validate_model_class()

    def validate_model_class(self):
        if not issubclass(self.model_class, models.Model):
            raise ValueError(
                "Data repository can only be configured for models")

    def get_model_object(self, **kwargs):
        return self.model_class(**kwargs)

    def get(self, locked=False, **kwargs):
        try:
            if locked:
                return self.model_class.objects.select_for_update(
                    nowait=True).get(**kwargs)
            else:
                return self.model_class.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            return None

    def filter(self, locked=False, query=None, **kwargs):
        queryset = self.model_class.objects.filter(**kwargs)
        if query:
            queryset = queryset.filter(query)
        if locked:
            return queryset.select_for_update(nowait=True)
        return queryset

    def create(self, **kwargs):
        return self.model_class.objects.create(**kwargs)

    def get_or_create(self, **kwargs):
        return self.model_class.objects.get_or_create(**kwargs)

    def update_or_create(self, **kwargs):
        return self.model_class.objects.update_or_create(**kwargs)

    def bulk_update(self, lst: list, fields: list, is_dict=False):
        if not is_dict:
            return self.model_class.objects.bulk_update(
                lst, fields, batch_size=500)
        return self.model_class.objects.bulk_update(
            [self.model_class(**i) for i in lst], fields, batch_size=500)

    def bulk_create(self, lst: list):
        return self.model_class.objects.bulk_create(lst, batch_size=500)