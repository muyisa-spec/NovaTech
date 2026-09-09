from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountTests(TestCase):
    def test_register_logs_the_new_user_in(self):
        response = self.client.post(reverse("register"), {
            "username": "ada", "email": "ada@example.test",
            "password1": "A-safe-password-2026", "password2": "A-safe-password-2026",
        })
        self.assertRedirects(response, reverse("account"))
        self.assertTrue(User.objects.filter(username="ada").exists())
