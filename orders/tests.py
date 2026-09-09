from decimal import Decimal
import hashlib
import hmac
import json
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from store.models import Category, Product
from .models import Order, OrderItem


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class CheckoutTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Audio", slug="audio")
        self.product = Product.objects.create(category=category, name="Enceinte", slug="enceinte", price=Decimal("20.00"), stock=4)
        session = self.client.session
        session["cart"] = {str(self.product.id): 2}
        session.save()

    def test_checkout_creates_order_reduces_stock_and_sends_emails(self):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(reverse("checkout"), {
                "first_name": "Ada", "last_name": "Lovelace", "email": "ada@example.test",
                "phone": "0100000000", "address": "1 rue Exemple", "city": "Kinshasa",
            })
        order = Order.objects.get()
        self.assertRedirects(response, reverse("order_success", args=[order.id]))
        self.assertEqual(order.total, Decimal("40.00"))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 2)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(len(mail.outbox), 2)

    def test_anonymous_user_cannot_view_another_order_confirmation(self):
        order = Order.objects.create(first_name="Autre", last_name="Client", email="x@example.test", phone="0", address="x", city="x")
        response = self.client.get(reverse("order_success", args=[order.id]))
        self.assertEqual(response.status_code, 404)

    def test_express_purchase_creates_pending_order_then_redirects_to_chariow(self):
        self.product.chariow_product_id = "prd_audio"
        self.product.chariow_payment_url = "https://sbbsojae.mychariow.shop/prd_4flawwm4/checkout"
        self.product.save()
        response = self.client.post(reverse("express_purchase", args=[self.product.id]), {
            "name": "Ada Lovelace", "email": "ada@example.test",
        })
        order = Order.objects.get(email="ada@example.test")
        self.assertRedirects(response, self.product.chariow_payment_url, fetch_redirect_response=False)
        self.assertEqual(order.status, Order.Status.PENDING)
        self.assertEqual(order.items.get().product, self.product)
        self.assertFalse(User.objects.filter(email="ada@example.test").exists())

    @override_settings(CHARIOW_WEBHOOK_SECRET="test-secret")
    def test_signed_webhook_confirms_order_and_creates_account(self):
        self.product.chariow_product_id = "prd_audio"
        self.product.save()
        order = Order.objects.create(first_name="Ada", last_name="Lovelace", email="ada@example.test", phone="", address="", city="", total=20)
        OrderItem.objects.create(order=order, product=self.product, product_name=self.product.name, price=self.product.price, quantity=1)
        payload = {"event": "successful.sale", "sale": {"id": "sal_123"}, "product": {"id": "prd_audio"}, "customer": {"email": "ada@example.test"}}
        body = json.dumps(payload).encode()
        signature = hmac.new(b"test-secret", body, hashlib.sha256).hexdigest()
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(reverse("chariow_webhook"), data=body, content_type="application/json", headers={"x-chariow-signature": f"sha256={signature}", "x-pulse-delivery-id": "delivery_123"})
        order.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(order.status, Order.Status.PAID)
        self.assertEqual(order.chariow_sale_id, "sal_123")
        self.assertEqual(User.objects.filter(email="ada@example.test").count(), 1)

    @override_settings(CHARIOW_WEBHOOK_SECRET="test-secret")
    def test_webhook_rejects_an_invalid_signature(self):
        response = self.client.post(
            reverse("chariow_webhook"), data=b'{"event":"successful.sale"}', content_type="application/json",
            headers={"x-chariow-signature": "sha256=invalid", "x-pulse-delivery-id": "delivery_invalid"},
        )
        self.assertEqual(response.status_code, 400)
