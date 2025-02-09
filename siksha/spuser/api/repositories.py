from _spbase.api.repositories import BaseRepository
from spuser.models import User, Profile


class UserRepository(BaseRepository):
    model_class = User


class ProfileRepository(BaseRepository):
    model_class = Profile
