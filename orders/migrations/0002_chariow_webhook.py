from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("orders", "0001_initial")]
    operations = [
        migrations.AddField(model_name="order", name="chariow_sale_id", field=models.CharField(blank=True, max_length=100, null=True, unique=True)),
        migrations.CreateModel(name="WebhookDelivery", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("delivery_id", models.CharField(max_length=100, unique=True)), ("event", models.CharField(max_length=80)), ("received_at", models.DateTimeField(auto_now_add=True))]),
    ]
