from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("nom", max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "catégorie"
        verbose_name_plural = "catégories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField("nom", max_length=180)
    slug = models.SlugField(unique=True)
    description = models.TextField("description", blank=True)
    price = models.DecimalField("prix", max_digits=10, decimal_places=2)
    currency = models.CharField("devise", max_length=8, default="$")
    image = models.ImageField("image", upload_to="products/", blank=True)
    stock = models.PositiveIntegerField("stock", default=0)
    chariow_product_id = models.CharField("identifiant produit Chariow", max_length=100, blank=True)
    chariow_payment_url = models.URLField("lien de paiement Chariow", blank=True)
    external_product_url = models.URLField("lien public du produit", blank=True)
    is_active = models.BooleanField("actif", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "produit"
        verbose_name_plural = "produits"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})


class SiteProfile(models.Model):
    """Informations publiques du fondateur, modifiables depuis l'administration."""
    founder_name = models.CharField("nom du fondateur", max_length=150, default="Muyisa Christian")
    bio = models.TextField(
        "présentation",
        default="Fondateur de NovaTech, passionné par la formation digitale et l'accompagnement des entrepreneurs vers l'autonomie numérique.",
    )
    photo = models.ImageField("photo du fondateur", upload_to="about/", blank=True)

    class Meta:
        verbose_name = "profil public"
        verbose_name_plural = "profil public"

    def __str__(self):
        return f"Profil public — {self.founder_name}"
