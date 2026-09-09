from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Category", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=100, unique=True, verbose_name="nom")), ("slug", models.SlugField(unique=True))], options={"verbose_name": "catégorie", "verbose_name_plural": "catégories", "ordering": ["name"]}),
        migrations.CreateModel(name="Product", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=180, verbose_name="nom")), ("slug", models.SlugField(unique=True)), ("description", models.TextField(blank=True, verbose_name="description")), ("price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="prix")), ("image", models.ImageField(blank=True, upload_to="products/", verbose_name="image")), ("stock", models.PositiveIntegerField(default=0, verbose_name="stock")), ("is_active", models.BooleanField(default=True, verbose_name="actif")), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="store.category"))], options={"verbose_name": "produit", "verbose_name_plural": "produits", "ordering": ["-created_at"]}),
    ]
