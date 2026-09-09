from django.db import migrations, models


def add_growth_hacking_product(apps, schema_editor):
    Category = apps.get_model("store", "Category")
    Product = apps.get_model("store", "Product")
    category, _ = Category.objects.get_or_create(name="Marketing Digital", defaults={"slug": "marketing-digital"})
    Product.objects.update_or_create(
        slug="formation-growth-hacking-reseaux-sociaux",
        defaults={
            "category": category,
            "name": "Formation Growth Hacking & Réseaux Sociaux",
            "description": "Les stratégies pour faire exploser ta visibilité et générer des clients grâce aux réseaux sociaux.",
            "price": "12.00",
            "currency": "$",
            "image": "products/growth-hacking-placeholder.svg",
            "stock": 999,
            "is_active": True,
            "chariow_product_id": "prd_4flawwm4",
            "chariow_payment_url": "https://sbbsojae.mychariow.shop/prd_4flawwm4/checkout",
            "external_product_url": "https://exemple.com/formation-growth-hacking",
        },
    )


class Migration(migrations.Migration):
    dependencies = [("store", "0003_siteprofile")]
    operations = [
        migrations.AddField(model_name="product", name="currency", field=models.CharField(default="$", max_length=8, verbose_name="devise")),
        migrations.AddField(model_name="product", name="external_product_url", field=models.URLField(blank=True, verbose_name="lien public du produit")),
        migrations.RunPython(add_growth_hacking_product, migrations.RunPython.noop),
    ]
