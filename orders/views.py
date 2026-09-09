import hashlib
import hmac
import json
from decimal import Decimal
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from store.models import Product
from .forms import CheckoutForm, ExpressPurchaseForm
from .models import Order, OrderItem, WebhookDelivery
from .services import confirm_paid_order


def express_purchase(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    if not product.chariow_payment_url:
        messages.error(request, "Le paiement de ce produit n'est pas encore configuré.")
        return redirect(product.get_absolute_url())
    form = ExpressPurchaseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        order = form.save(commit=False)
        order.total = product.price
        order.currency = product.currency
        order.status = Order.Status.PENDING
        order.save()
        OrderItem.objects.create(order=order, product=product, product_name=product.name, price=product.price, quantity=1)
        return redirect(product.chariow_payment_url)
    return render(request, "orders/express_purchase.html", {"form": form, "product": product})


def checkout(request):
    cart = request.session.get("cart", {})
    products = Product.objects.filter(id__in=cart, is_active=True)
    lines, total = [], Decimal("0.00")
    for product in products:
        try:
            requested_quantity = int(cart.get(str(product.id), 0))
        except (TypeError, ValueError):
            requested_quantity = 0
        quantity = min(max(requested_quantity, 0), product.stock)
        if quantity:
            lines.append((product, quantity))
            total += product.price * quantity
    if not lines:
        messages.warning(request, "Votre panier est vide.")
        return redirect("cart")
    initial = {}
    if request.user.is_authenticated:
        initial = {"first_name": request.user.first_name, "last_name": request.user.last_name, "email": request.user.email}
    form = CheckoutForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.total = total
            order.currency = lines[0][0].currency
            order.save()
            for product, quantity in lines:
                Product.objects.filter(pk=product.pk, stock__gte=quantity).update(stock=product.stock - quantity)
                OrderItem.objects.create(order=order, product=product, product_name=product.name, price=product.price, quantity=quantity)
        request.session["cart"] = {}
        request.session["last_order_id"] = order.pk
        transaction.on_commit(lambda: send_order_notifications(order))
        messages.success(request, f"Votre commande #{order.pk} a bien été enregistrée.")
        return redirect("order_success", order_id=order.pk)
    return render(request, "orders/checkout.html", {"form": form, "total": total, "lines": lines})


def success(request, order_id):
    order = Order.objects.filter(pk=order_id).first()
    if not order or (order.user_id and order.user_id != request.user.id) or (not order.user_id and request.session.get("last_order_id") != order.pk):
        raise Http404
    return render(request, "orders/success.html", {"order": order})


@csrf_exempt
@require_POST
def chariow_webhook(request):
    """Confirme un achat seulement après vérification HMAC de Chariow."""
    secret = settings.CHARIOW_WEBHOOK_SECRET.encode()
    supplied = request.headers.get("x-chariow-signature", "")
    if not secret or not supplied.startswith("sha256="):
        return HttpResponseBadRequest("Signature manquante")
    expected = hmac.new(secret, request.body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(supplied.removeprefix("sha256="), expected):
        return HttpResponseBadRequest("Signature invalide")
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("JSON invalide")
    delivery_id = request.headers.get("x-pulse-delivery-id")
    if not delivery_id:
        return HttpResponseBadRequest("Identifiant de livraison manquant")
    delivery, created = WebhookDelivery.objects.get_or_create(
        delivery_id=delivery_id, defaults={"event": payload.get("event", "")}
    )
    if not created or payload.get("event") != "successful.sale":
        return JsonResponse({"ok": True})
    sale = payload.get("sale", {})
    metadata = sale.get("custom_metadata") or {}
    order = None
    if metadata.get("order_ref"):
        order = Order.objects.filter(pk=metadata["order_ref"], status=Order.Status.PENDING).first()
    if order is None:
        email = (payload.get("customer") or {}).get("email", "")
        product_id = (payload.get("product") or {}).get("id", "")
        candidates = Order.objects.filter(
            status=Order.Status.PENDING, email__iexact=email,
            items__product__chariow_product_id=product_id,
        ).distinct().order_by("-created_at")
        if candidates.count() == 1:
            order = candidates.first()
    if order is None:
        return JsonResponse({"ok": True, "matched": False})
    confirm_paid_order(order, sale.get("id", ""))
    return JsonResponse({"ok": True, "matched": True})


def send_order_notifications(order):
    """Envoie les confirmations seulement une fois la transaction validée."""
    customer_message = (
        f"Bonjour {order.first_name},\n\n"
        f"Votre commande #{order.pk}, d'un montant de {order.total} €, a été reçue."
    )
    send_mail(
        subject=f"Confirmation de votre commande #{order.pk}",
        message=customer_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.email],
        fail_silently=True,
    )
    if settings.ADMIN_NOTIFICATION_EMAIL:
        send_mail(
            subject=f"Nouvelle commande #{order.pk}",
            message=f"{order.first_name} {order.last_name} vient de commander pour {order.total} €.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
            fail_silently=True,
        )
