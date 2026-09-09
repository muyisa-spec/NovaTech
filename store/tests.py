from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from .models import Category, Product


class StoreViewsTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Accessoires", slug="accessoires")
        self.product = Product.objects.create(
            category=category, name="Casque", slug="casque", price=Decimal("59.90"), stock=3
        )

    def test_catalogue_is_available(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Casque")

    def test_add_and_update_cart(self):
        self.client.post(reverse("add_to_cart", args=[self.product.id]))
        response = self.client.post(
            reverse("update_cart", args=[self.product.id]),
            {"quantity": 2},
            follow=True,
        )
        self.assertContains(response, "119,80")

    def test_invalid_cart_quantity_is_safe(self):
        session = self.client.session
        session["cart"] = {str(self.product.id): "not-a-number"}
        session.save()
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)
