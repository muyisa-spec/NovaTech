from decimal import Decimal
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Product, SiteProfile


def home(request):
    products = Product.objects.filter(is_active=True).select_related("category")
    return render(request, "store/home.html", {"products": products, "categories": Category.objects.all()})


def product_detail(request, slug):
    return render(request, "store/product_detail.html", {"product": get_object_or_404(Product, slug=slug, is_active=True)})


def about(request):
    profile, _ = SiteProfile.objects.get_or_create(
        pk=1,
        defaults={
            "founder_name": "Muyisa Christian",
            "bio": "Fondateur de NovaTech, passionné par la formation digitale et l'accompagnement des entrepreneurs vers l'autonomie numérique.",
            "photo": "about/fondateur.jpg",
        },
    )
    return render(request, "store/about.html", {"profile": profile})


def cart(request):
    cart_data = request.session.get("cart", {})
    products = Product.objects.filter(id__in=cart_data, is_active=True)
    items, total = [], Decimal("0.00")
    for product in products:
        try:
            requested_quantity = int(cart_data.get(str(product.id), 0))
        except (TypeError, ValueError):
            requested_quantity = 0
        quantity = min(max(requested_quantity, 0), product.stock)
        if quantity:
            subtotal = product.price * quantity
            total += subtotal
            items.append({"product": product, "quantity": quantity, "subtotal": subtotal})
    return render(request, "store/cart.html", {"items": items, "total": total})


def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("home")
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart_data = request.session.get("cart", {})
    try:
        current = int(cart_data.get(str(product.id), 0))
    except (TypeError, ValueError):
        current = 0
    cart_data[str(product.id)] = min(current + 1, product.stock)
    request.session["cart"] = cart_data
    request.session.modified = True
    messages.success(request, f"{product.name} a été ajouté au panier.")
    return redirect("cart")


def update_cart(request, product_id):
    if request.method == "POST":
        cart_data = request.session.get("cart", {})
        try:
            quantity = max(0, int(request.POST.get("quantity", 0)))
        except (TypeError, ValueError):
            quantity = 0
        product = get_object_or_404(Product, id=product_id, is_active=True)
        if quantity:
            cart_data[str(product.id)] = min(quantity, product.stock)
        else:
            cart_data.pop(str(product.id), None)
        request.session["cart"] = cart_data
        request.session.modified = True
    return redirect("cart")
