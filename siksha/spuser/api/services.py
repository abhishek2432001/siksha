from spuser.api.repositories import UserRepository, ProfileRepository


class UserService:

    user_repository = UserRepository
    profile_repository = ProfileRepository

    def signup(self, request):
        err_list = []
        response = None
        token = ""
        data = request.data
        password = data.get("password")
        email = data.get("email")
        name = data.get("name")
        if not (email and password and name):
            err_list.append({
                "message": "Email, password and name are required",
                "code": 100
            })
        if err_list:
            return {
                "success": False,
                "error_list": err_list,
                "error": "Validation Failed",
                "code": 400
            }
        user = self.user_repository
        self.user_repository.create(email=email, password=password, name=name)


        return {"success": True, "token": token}

    def login(self, request):
        error = None
        response = None
        token = ""
        return {"success": True, "token": token}


