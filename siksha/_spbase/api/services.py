from django.conf import settings

from _spbase.helpers.validation_helper import Validators


class BaseApiService:

    @staticmethod
    def get_no_count_paginator(
            page_number, data, limit=settings.DEFAULT_PAGE_LIMIT):
        page_number, limit, _ = Validators.paginate_params_validator(
            page_number, limit)
        start_index = (page_number - 1) * limit
        end_index = start_index + limit + 1
        # Fetch one extra item to check for next page
        object_list = list(data[start_index:end_index])
        has_next = len(object_list) > limit
        has_previous = page_number > 1
        if has_next:
            object_list = object_list[:limit]  # Trim the extra item
        return object_list, {
            'has_previous': has_previous,
            'has_next': has_next,
            'page_size': limit,
            'current_page': page_number}