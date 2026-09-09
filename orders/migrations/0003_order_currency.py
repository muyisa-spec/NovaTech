from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("orders", "0002_chariow_webhook")]
    operations = [
        migrations.AddField(model_name="order", name="currency", field=models.CharField(default="$", max_length=8, verbose_name="devise")),
    ]
