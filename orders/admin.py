from django.contrib import admin
from .models import Order, OrderItem, WebhookDelivery
from .services import confirm_paid_order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "price", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "total", "status", "created_at")
    list_filter = ("status", "created_at")
    inlines = [OrderItemInline]
    actions = ["mark_as_paid"]

    @admin.action(description="Confirmer les commandes sélectionnées comme payées")
    def mark_as_paid(self, request, queryset):
        confirmed = 0
        for order in queryset.exclude(status=Order.Status.PAID):
            confirm_paid_order(order)
            confirmed += 1
        self.message_user(request, f"{confirmed} commande(s) confirmée(s).")


@admin.register(WebhookDelivery)
class WebhookDeliveryAdmin(admin.ModelAdmin):
    list_display = ("delivery_id", "event", "received_at")
    readonly_fields = ("delivery_id", "event", "received_at")
    search_fields = ("delivery_id",)
