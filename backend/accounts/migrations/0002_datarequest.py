# Generated for APOCAL'IPSSI J3-bis RGPD.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DataRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("requested_at", models.DateTimeField(auto_now_add=True)),
                ("responded_at", models.DateTimeField(blank=True, null=True)),
                ("status", models.CharField(choices=[("received", "Reçue"), ("processing", "En cours"), ("responded", "Répondue"), ("failed", "Échec")], default="received", max_length=20)),
                ("export_format", models.CharField(default="json", max_length=10)),
                ("file_hash", models.CharField(blank=True, max_length=64)),
                ("scope", models.JSONField(blank=True, default=list)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("user_agent", models.TextField(blank=True)),
                ("user", models.ForeignKey(help_text="Utilisateur ayant demandé l'accès à ses données.", on_delete=django.db.models.deletion.CASCADE, related_name="data_requests", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Demande RGPD",
                "verbose_name_plural": "Demandes RGPD",
                "ordering": ["-requested_at"],
            },
        ),
    ]
