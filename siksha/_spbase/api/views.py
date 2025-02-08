from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from spauth.auth import UserAuthTokenAuthentication


class NoAuthViewSet(ViewSet):

    class Meta:
        abstract = True


class SessionAuthViewSet(ViewSet):

    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    class Meta:
        abstract = True


class AllAuthViewSet(ViewSet):
    authentication_classes = SessionAuthentication
    permission_classes = (IsAuthenticated, )

    class Meta:
        abstract = True


class TokenAuthViewSet(ViewSet):
    authentication_classes = (UserAuthTokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    class Meta:
        abstract = True
