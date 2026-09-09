from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Adresse e-mail", required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {"username": "Nom d'utilisateur"}


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Adresse e-mail")

    def clean(self):
        email = self.cleaned_data.get("username", "").strip()
        if email:
            user = User.objects.filter(email__iexact=email).order_by("id").first()
            if user:
                self.cleaned_data["username"] = user.username
        return super().clean()
