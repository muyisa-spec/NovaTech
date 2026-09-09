from django.db import migrations, models


def create_site_profile(apps, schema_editor):
    SiteProfile = apps.get_model("store", "SiteProfile")
    SiteProfile.objects.get_or_create(
        pk=1,
        defaults={
            "founder_name": "Muyisa Christian",
            "bio": "Fondateur de NovaTech, passionné par la formation digitale et l'accompagnement des entrepreneurs vers l'autonomie numérique.",
            "photo": "about/fondateur.jpg",
        },
    )


class Migration(migrations.Migration):
    dependencies = [("store", "0002_chariow_fields")]
    operations = [
        migrations.CreateModel(
            name="SiteProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("founder_name", models.CharField(default="Muyisa Christian", max_length=150, verbose_name="nom du fondateur")),
                ("bio", models.TextField(default="Fondateur de NovaTech, passionné par la formation digitale et l'accompagnement des entrepreneurs vers l'autonomie numérique.", verbose_name="présentation")),
                ("photo", models.ImageField(blank=True, upload_to="about/", verbose_name="photo du fondateur")),
            ],
            options={"verbose_name": "profil public", "verbose_name_plural": "profil public"},
        ),
        migrations.RunPython(create_site_profile, migrations.RunPython.noop),
    ]
