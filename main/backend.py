from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            print(f"Usuario encontrado: {user}")
        except UserModel.DoesNotExist:
            return None
        else:
            print(f"Check password: {user.check_password(password)}")
            print(f"User can authenticate: {self.user_can_authenticate(user)}")
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
