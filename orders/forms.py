from django import forms
from django.forms import ModelForm
from .models import Order


class ExpressPurchaseForm(ModelForm):
    name = forms.CharField(label="Nom complet", max_length=160)

    class Meta:
        model = Order
        fields = ("email",)
        labels = {"email": "Adresse e-mail"}

    def save(self, commit=True):
        order = super().save(commit=False)
        parts = self.cleaned_data["name"].strip().split(maxsplit=1)
        order.first_name = parts[0]
        order.last_name = parts[1] if len(parts) > 1 else ""
        if commit:
            order.save()
        return order


class CheckoutForm(ModelForm):
    class Meta:
        model = Order
        fields = ("first_name", "last_name", "email", "phone", "address", "city")
