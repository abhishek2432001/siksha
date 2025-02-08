import datetime
import math
import re

from django.conf import settings


class Validators:

    @staticmethod
    def datetime_validator(
            date_string, date_fmt="%Y-%m-%d %H:%M:%S", timezone_aware=False):
        valid_date = False
        formatted_datetime = None
        try:
            formatted_datetime = datetime.datetime.strptime(
                date_string, date_fmt)
            if timezone_aware:
                formatted_datetime = formatted_datetime.replace(
                    tzinfo=datetime.timezone.utc)
            valid_date = True
        except Exception:
            pass
        return formatted_datetime, valid_date

    @staticmethod
    def date_validator(date_string, date_fmt="%Y-%m-%d"):
        valid_date = False
        formatted_date = None
        try:
            formatted_date = datetime.datetime.strptime(
                date_string, date_fmt).date()
            valid_date = True
        except Exception:
            pass
        return formatted_date, valid_date

    @staticmethod
    def time_validator(time_string):
        valid_date = False
        formatted_time = None
        try:
            formatted_time = datetime.datetime.strptime(
                time_string, "%H:%M:%S").time()
            valid_date = True
        except Exception:
            pass
        return formatted_time, valid_date

    @staticmethod
    def float_validator(val):
        valid_float = False
        result = 0.0
        try:
            result = float(val)
            if math.isnan(result):
                return result, valid_float
            valid_float = True
        except Exception:
            pass
        return result, valid_float

    @staticmethod
    def int_validator(val, positive_only=False):
        valid_int = False
        result = 0
        try:
            result = int(val)
            if positive_only and result <= 0:
                return None, False
            valid_int = True
        except Exception:
            pass
        return result, valid_int

    @staticmethod
    def boolean_validator(val):
        if isinstance(val, bool):
            return True
        return False

    @staticmethod
    def bool_value(val):
        if val in ['0', 0, 'false', False]:
            return False, True
        if val in ['1', 1, 'true', True]:
            return True, True
        return None, False

    @staticmethod
    def list_of_string_validator(val):
        if isinstance(val, list):
            for v in val:
                if not isinstance(v, str):
                    return False
            return True
        return False

    @staticmethod
    def list_of_int_validator(val, positive_only=False):
        if isinstance(val, list):
            input_data = val
        elif isinstance(val, str):
            input_data = val.split(',')
        else:
            return None, False
        output = []
        for data in input_data:
            data, valid = Validators.int_validator(data)
            if not valid:
                return None, False
            if positive_only and data <= 0:
                return None, False
            output.append(data)
        return output, True

    @staticmethod
    def check_valid_email(email):
        if not email:
            return False
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_validation = re.fullmatch(email_regex, email)
        if email_validation:
            return True
        else:
            return False

    @staticmethod
    def check_valid_phone_number(phone_number):
        if not phone_number:
            return False
        phone_regex = re.compile(r'^\d{10}$')
        phone_validation = phone_regex.match(phone_number)
        if phone_validation:
            return True
        return False

    @staticmethod
    def validator_map():
        validator_map = {
            'int': 'int_validator',
            'float': 'float_validator',
            'str': 'str_validator',
            'boolean': 'boolean_validator',
            'int_list': 'int_list_validator',
            'time': 'time_validator'
        }
        return validator_map

    @staticmethod
    def validation_functions(data_type, value):
        result = value
        status = False
        if not (value and data_type):
            return "enter the value or data type to be validated", status
        validator_map = Validators.validator_map()
        function_name = validator_map.get(data_type, None)
        if not function_name:
            return "data type not defined", status
        if function_name == 'int_validator':
            result, status = Validators.int_validator(value)
        if function_name == 'float_validator':
            result, status = Validators.float_validator(value)
        if function_name == 'str_validator':
            status = True
        if function_name == 'boolean_validator':
            status = Validators.boolean_validator(value)
        if function_name == 'int_list_validator':
            result, status = Validators.list_of_int_validator(value)
        if function_name == 'time_validator':
            result, status = Validators.time_validator(value)
        return result, status

    @staticmethod
    def url_validator(url):
        url_re = r"^((https?|ftp|smtp):\/\/)?(www.)?[a-z0-9]+\.[a-z]+(\/[a-zA-Z0-9#]+\/?)*"
        url_val = re.compile(url_re)
        if re.search(url_val, url):
            return url, True
        return None, False

    @staticmethod
    def validate_using_regex(input_value, regex):
        try:
            compiled_value = re.compile(regex)
            if re.search(compiled_value, input_value):
                return True
        except Exception:
            pass
        return False

    @staticmethod
    def paginate_params_validator(page_no, limit):
        page_no, is_valid = Validators.int_validator(page_no)
        if not is_valid or page_no < 1:
            page_no = 1
        limit, is_valid = Validators.int_validator(limit)
        if not is_valid or limit < 1:
            limit = settings.DEFAULT_PAGE_LIMIT
        return page_no, limit, True

    def pin_code_validator(pin_code):  # pincode validator
        if pin_code is None:
            return False
        regex = "^[1-9][0-9]{5}$"
        pin = re.compile(regex)
        if re.search(pin, pin_code):
            return True
        return str(pin_code), False