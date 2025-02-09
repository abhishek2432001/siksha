from _spbase.api.views import TokenAuthViewSet
from spuser.api.services import UserService


class UserViewSet(TokenAuthViewSet):
    service_class = UserService

    def login(self, request):
        return self.service_class.login(request)