from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("store", "0001_initial")]
    operations = [
        migrations.CreateModel(name="Order", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("first_name", models.CharField(max_length=80, verbose_name="prénom")), ("last_name", models.CharField(max_length=80, verbose_name="nom")), ("email", models.EmailField(max_length=254)), ("phone", models.CharField(max_length=30, verbose_name="téléphone")), ("address", models.TextField(verbose_name="adresse")), ("city", models.CharField(max_length=100, verbose_name="ville")), ("total", models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="total")), ("status", models.CharField(choices=[("pending", "En attente"), ("paid", "Payée"), ("shipped", "Expédiée"), ("cancelled", "Annulée")], default="pending", max_length=20)), ("created_at", models.DateTimeField(auto_now_add=True)), ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="orders", to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name="OrderItem", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("product_name", models.CharField(max_length=180)), ("price", models.DecimalField(decimal_places=2, max_digits=10)), ("quantity", models.PositiveIntegerField()), ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="orders.order")), ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="store.product"))]),
    ]
