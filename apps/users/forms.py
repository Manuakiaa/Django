# Django modules
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# Project modules
from apps.users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Form of the admin "Add gamer" page. Password is hashed on save."""

    class Meta:
        """Meta data of the form."""

        model = CustomUser
        fields = ("email", "nickname")


class CustomUserChangeForm(UserChangeForm):
    """Form of the admin "Change gamer" page."""

    class Meta:
        """Meta data of the form."""

        model = CustomUser
        fields = "__all__"
