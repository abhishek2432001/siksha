import jwt


from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from spuser.models import User


class UserAuthTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_data = request.headers.get('Authorization')
        if not auth_data:
            raise AuthenticationFailed('Please provide token for authorization')
        auth_value = auth_data.split()
        if len(auth_value) != 2:
            raise AuthenticationFailed('Invalid token format')
        token = auth_value[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except Exception as e:
            raise AuthenticationFailed('Invalid token')

        return user, token