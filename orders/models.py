from django.conf import settings
from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        PAID = "paid", "Payée"
        SHIPPED = "shipped", "Expédiée"
        CANCELLED = "cancelled", "Annulée"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    first_name = models.CharField("prénom", max_length=80)
    last_name = models.CharField("nom", max_length=80)
    email = models.EmailField()
    phone = models.CharField("téléphone", max_length=30)
    address = models.TextField("adresse")
    city = models.CharField("ville", max_length=100)
    total = models.DecimalField("total", max_digits=10, decimal_places=2, default=0)
    currency = models.CharField("devise", max_length=8, default="$")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    chariow_sale_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Commande #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("store.Product", on_delete=models.PROTECT)
    product_name = models.CharField(max_length=180)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.price * self.quantity


class WebhookDelivery(models.Model):
    delivery_id = models.CharField(max_length=100, unique=True)
    event = models.CharField(max_length=80)
    received_at = models.DateTimeField(auto_now_add=True)
