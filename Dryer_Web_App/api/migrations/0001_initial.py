# Generated by Django 3.2.15 on 2022-11-28 15:54

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        default=api.models.generate_unique_code,
                        max_length=8,
                        unique=True,
                    ),
                ),
                ("orderer_name", models.CharField(default="", max_length=20)),
                ("orderer_surname", models.CharField(default="", max_length=20)),
                ("dryer_model", models.CharField(default="", max_length=10)),
                ("create_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]