from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("a-propos/", views.about, name="about"),
    path("produits/<slug:slug>/", views.product_detail, name="product_detail"),
    path("panier/", views.cart, name="cart"),
    path("panier/ajouter/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("panier/modifier/<int:product_id>/", views.update_cart, name="update_cart"),
]
