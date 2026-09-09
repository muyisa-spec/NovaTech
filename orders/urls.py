from django.urls import path
from . import views

urlpatterns = [
    path("acheter/<int:product_id>/", views.express_purchase, name="express_purchase"),
    path("validation/", views.checkout, name="checkout"),
    path("confirmation/<int:order_id>/", views.success, name="order_success"),
    path("webhooks/chariow/", views.chariow_webhook, name="chariow_webhook"),
]
