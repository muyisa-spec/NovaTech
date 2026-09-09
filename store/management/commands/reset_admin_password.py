"""Réinitialise temporairement le mot de passe d'un superutilisateur via une variable d'environnement."""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Réinitialise le mot de passe du premier superutilisateur si ADMIN_RESET_PASSWORD est défini."

    def handle(self, *args, **options):
        password = os.getenv("ADMIN_RESET_PASSWORD")
        if not password:
            self.stdout.write("ADMIN_RESET_PASSWORD absent : aucune modification.")
            return

        user = get_user_model().objects.filter(is_superuser=True).order_by("id").first()
        if user is None:
            self.stdout.write(self.style.WARNING("Aucun superutilisateur à modifier."))
            return

        user.set_password(password)
        user.save(update_fields=["password"])
        self.stdout.write(self.style.SUCCESS(f"Mot de passe réinitialisé pour {user.get_username()}."))
