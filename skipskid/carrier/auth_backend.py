from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import Carrier


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        
        user_models = [Carrier]  # Assuming Carrier, Shipper, and Business are your custom user models
        for UserModel in user_models:
            try:
                user = UserModel.objects.get(email__iexact=email)
                if user.check_password(password):
                    return user
            except UserModel.DoesNotExist:
                pass
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        