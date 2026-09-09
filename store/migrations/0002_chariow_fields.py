from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("store", "0001_initial")]
    operations = [
        migrations.AddField(model_name="product", name="chariow_product_id", field=models.CharField(blank=True, max_length=100, verbose_name="identifiant produit Chariow")),
        migrations.AddField(model_name="product", name="chariow_payment_url", field=models.URLField(blank=True, verbose_name="lien de paiement Chariow")),
    ]
