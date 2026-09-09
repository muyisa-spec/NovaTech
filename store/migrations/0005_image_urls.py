from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("store", "0004_product_currency_external_link")]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image_url",
            field=models.URLField(blank=True, verbose_name="URL de l'image"),
        ),
        migrations.AddField(
            model_name="siteprofile",
            name="photo_url",
            field=models.URLField(blank=True, verbose_name="URL de la photo"),
        ),
    ]
