import datetime
import jwt
import pytz

from django.conf import settings


class GenerateToken:

    @staticmethod
    def generate_jwt_token(user):

        token = None
        try:
            payload = {
                'user_id': user.id,
                'username': user.first_name,
                'exp': datetime.datetime.now(tz=(pytz.timezone(settings.TIME_ZONE))) + datetime.timedelta(days=1),
                'iat': datetime.datetime.now(tz=(pytz.timezone(settings.TIME_ZONE)))

            }

            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        except:
            pass

        return token
