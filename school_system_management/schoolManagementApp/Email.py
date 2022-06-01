from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


# FUNCTIE SEPARATA PENTRU AUTENTIFICAREA CU EMAIL SI PAROLA
class Email(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        model = get_user_model();
        try:
            user = model.objects.get(email=username)
        except model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            else:
                return None
