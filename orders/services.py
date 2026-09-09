import secrets

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import Order


def username_for_email(email):
    base = email.split("@", 1)[0][:120] or "client"
    candidate, suffix = base, 1
    while User.objects.filter(username=candidate).exists():
        suffix += 1
        candidate = f"{base[:145 - len(str(suffix))]}-{suffix}"
    return candidate


def attach_account(order):
    """Rattache la commande à l'utilisateur existant ou crée son accès."""
    user = User.objects.filter(email__iexact=order.email).order_by("id").first()
    created = user is None
    if created:
        user = User.objects.create_user(
            username=username_for_email(order.email), email=order.email,
            first_name=order.first_name, last_name=order.last_name, password=secrets.token_urlsafe(32),
        )
    if order.user_id != user.id:
        order.user = user
        order.save(update_fields=["user"])
    return user, created


@transaction.atomic
def confirm_paid_order(order, sale_id=""):
    """Opération idempotente utilisable depuis le webhook comme l'administration."""
    order = Order.objects.select_for_update().get(pk=order.pk)
    if order.status == Order.Status.PAID:
        return order, False
    order.status = Order.Status.PAID
    if sale_id:
        order.chariow_sale_id = sale_id
    order.save(update_fields=["status", "chariow_sale_id"])
    user, created = attach_account(order)
    transaction.on_commit(lambda: send_purchase_emails(order, user, created))
    return order, True


def send_purchase_emails(order, user, account_created):
    product = order.items.select_related("product").first().product
    product_url = f"{settings.SITE_URL}{product.get_absolute_url()}"
    message = (
        f"Bonjour {order.first_name},\n\nVotre paiement est confirmé. "
        f"Accédez directement à votre achat : {product_url}\n"
    )
    if account_created:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        password_url = f"{settings.SITE_URL}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"
        message += f"\nVotre espace personnel a été créé. Choisissez votre mot de passe ici : {password_url}\n"
    else:
        message += f"\nRetrouvez vos achats dans votre espace : {settings.SITE_URL}{reverse('account')}\n"
    send_mail(
        subject=f"Paiement confirmé — commande #{order.pk}", message=message,
        from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[order.email], fail_silently=True,
    )
